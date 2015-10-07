#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import os

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
BASE_DIR = os.path.abspath('.') 

class Chrome():
    def __init__(self,url):
        self.init_driver()
        self.start(url)
        self.end()

    def init_driver(self):
        chromedriver = os.path.join(BASE_DIR, 'services/chromedriver_ubuntu')
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
    def start(self,url):
    	self.driver.load(url)
    	elem = driver.find_element_by_name("q")
	elem.send_keys("pycon")
	elem.send_keys(Keys.RETURN)
    def stop(self):
	self.driver.close

Chrome("http://www.python.org")




# class Browser():
# 	def __init__(self):
# 		self.driver = webdriver.Firefox()
# 		assert "Python" in driver.title
# 		self.load("http://www.python.org")
# 		assert "No results found." not in driver.page_source
# 		self.driver.close()
# 	def load(self,url):
# 		self.driver.get(url)
# 		elem = driver.find_element_by_name("q")
# 		elem.send_keys("pycon")
# 		elem.send_keys(Keys.RETURN)
# Browser()


