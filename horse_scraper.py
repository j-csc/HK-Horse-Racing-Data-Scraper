#import libraries 
import requests
import string
import json
import itertools 
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from bs4 import BeautifulSoup

#starting the webdriver
driver = webdriver.Firefox()
driver.get('http://www.hkjc.com/english/racing/SelectHorse.asp')
alphabets = string.ascii_uppercase
wait = WebDriverWait(driver, 10)

def check_exists_by_xpath(xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True


names = list() 
country_of_origin_age = list() 
colour_sex = list() 
import_type = list() 
season_stakes = list() 
total_stakes = list() 
no_of_123_starts = list() 
no_of_starts_in_past_races = list() 
trainer = list() 
owner = list() 
current_rating = list() 
start_of_season_rating = list() 
sire = list() 
dam = list() 
dam_sire = list()

alphabet_link = "http://racing.hkjc.com/racing/information/English/Horse/SelectHorsebyChar.aspx?ordertype="

horse_link_xpath = "//p/table/tbody/tr[2]/td/table/tbody"

for i in alphabets:
  driver.get(alphabet_link + i)
  driver.implicitly_wait(10)
  horse_links = driver.find_elements_by_xpath(horse_link_xpath)
  for h in horse_links:
    row_links = h.find_elements_by_tag_name("a")
    for item in row_links:
      print(item.text)
