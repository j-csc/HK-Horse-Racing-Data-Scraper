#import libraries
from bs4 import BeautifulSoup
import requests
import string
import os.path
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import Select

import re

def get_dates():
  res = []
  BASE_URL = "https://racing.hkjc.com/racing/information/English/racing/LocalResults.aspx"

  dates_xpath = "/html/body/div/div[3]/p[1]/span[2]/select"

  driver = webdriver.Firefox()
  wait = WebDriverWait(driver, 10)

  def check_exists_by_xpath(xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True

  driver.get(BASE_URL)
  driver.implicitly_wait(20)
  if (check_exists_by_xpath(dates_xpath)):
    dates_select = (driver.find_elements_by_xpath(dates_xpath))
    temp_text = (dates_select[0].text)
    res = temp_text.split('\n')
  return res

if __name__ == "__main__":
  print(get_dates())