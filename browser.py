#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import os

from pyvirtualdisplay import Display
from selenium import webdriver
from tld import get_tld
import boto
import boto.s3.connection

from config import BASE_DIR, OS_NAME, S3_ACCESS_KEY, S3_SECRET_KEY
from  extensions import ExtensionsParser

class Browser:
    def start_service(self, display_options):
        self.display = Display(**display_options)
        self.display.start()

    def stop_service(self):
        self.driver.quit()
        if OS_NAME == 'linux2':
            self.display.stop()

    def close_another_tabs(self):
        handles = self.driver.window_handles
        time.sleep(3)
        for h in handles:
            if h != handles[0]:
                self.driver.switch_to_window(h)
                self.driver.close()
        self.driver.switch_to_window(self.driver.window_handles[0])

    def get_data(self, site_url, country_code):
        print 'get_data url(%s)=%s'%(country_code, site_url)
        self.driver.set_window_size(1920, 1080)
        self.driver.get(site_url)
        time.sleep(15)

        if len(self.driver.window_handles) > 1:
            self.close_another_tabs()

        extensions_parser = ExtensionsParser(self.driver)
        # time.sleep(250)

        return {
            'screen_path': self.save_screenshot_s3(site_url, country_code),
            'extesions_products': extensions_parser.find_extension()
        }

    def save_screenshot(self, site_url, country_code):
        if not os.path.exists('%s/screenshots/%s' % (BASE_DIR, self.screenshot_daily_folder)):
            os.mkdir('%s/screenshots/%s' % (BASE_DIR, self.screenshot_daily_folder))

        screen_path = '%s/screenshots/%s/%s_%s_%s.png' % (BASE_DIR, self.screenshot_daily_folder, get_tld(site_url).replace('.', '_'), country_code, int(time.time()))
        print 'screen_path=', screen_path
        self.driver.get_screenshot_as_file(screen_path)
        time.sleep(4)
        return screen_path

    def save_screenshot_s3(self, site_url, country_code):
        conn = boto.connect_s3(
            aws_access_key_id = S3_ACCESS_KEY,
            aws_secret_access_key = S3_SECRET_KEY,
            #is_secure=False,               # uncommmnt if you are not using ssl
            calling_format = boto.s3.connection.OrdinaryCallingFormat(),
        )
        bucket = conn.get_bucket('synergetica')
        key = bucket.new_key('%s/%s_%s_%s.png'%(self.screenshot_daily_folder, get_tld(site_url).replace('.', '_'), country_code, int(time.time())))
        key.set_contents_from_string(self.driver.get_screenshot_as_base64().decode('base64'))
        key.set_acl('public-read')
        url = key.generate_url(expires_in=0, query_auth=False, force_http=True)

        time.sleep(4)

        print 'screen_url=', url
        return url


class Chrome(Browser):
    def __init__(self, display_options):
        self.browser_name = 'chrome'
        self.screenshot_daily_folder = time.strftime("%Y-%m-%d")

        if OS_NAME == 'linux2':
            self.start_service(display_options)
        self.init_driver()

    def init_driver(self):
        if OS_NAME == 'win32':
            driver_name = 'chromedriver_win32'
        if OS_NAME == 'darwin':
            driver_name = 'chromedriver_mac'
        else:
            driver_name = 'chromedriver_ubuntu'

        chromedriver = os.path.join(BASE_DIR, 'services/' + driver_name)
        os.environ["webdriver.chrome.driver"] = chromedriver

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument("--test-type")
        chrome_options.add_extension('%s/extensions/chrome/1stOffer-SmartSlider_v1.3.3.crx' % (BASE_DIR))
        chrome_options.add_extension('%s/extensions/chrome/ask.crx' % (BASE_DIR))
        chrome_options.add_extension('%s/extensions/chrome/jolly.crx' % (BASE_DIR))
        chrome_options.add_extension('%s/extensions/chrome/omg-music-plus.crx' % (BASE_DIR))
        chrome_options.add_extension('%s/extensions/chrome/pricedetect.crx' % (BASE_DIR))
        chrome_options.add_extension('%s/extensions/chrome/pricegong.crx' % (BASE_DIR))
        chrome_options.add_extension('%s/extensions/chrome/shoppingate.crx' % (BASE_DIR))
        chrome_options.add_extension('%s/extensions/chrome/Shopzy_v0.9.22.1.crx' % (BASE_DIR))
        chrome_options.add_extension('%s/extensions/chrome/That-is-Worth_v1.8.1.0.crx' % (BASE_DIR))
        chrome_options.add_extension('%s/extensions/chrome/Top-Deal-Master_v1.0.2.crx' % (BASE_DIR))
        chrome_options.add_extension('%s/extensions/chrome/PriceBlink_v4.4.crx' % (BASE_DIR))

        self.driver = webdriver.Chrome(chromedriver, chrome_options=chrome_options)
