#import libraries
from bs4 import BeautifulSoup
import requests
import string
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

#starting webdriver
BASE_URL = "https://racing.hkjc.com/racing/information/English/racing/LocalResults.aspx"

driver = webdriver.Firefox()
driver.get(BASE_URL)
driver.implicitly_wait(50)

def check_exists_by_xpath(xpath):
  try:
      driver.find_element_by_xpath(xpath)
  except NoSuchElementException:
      return False
  return True

"""
Initialize variables: 

Data collected per entry: 
  place, horse_no, horse, jockey, trainer, actual_wt,
  declare_horse_wt, draw, lbw, running_pos, finish_time, win_odds
"""

race_name_xpath = "/html/body/div/div[4]/table/thead/tr/td[1]"
race_type_xpath = "/html/body/div/div[4]/table/tbody/tr[2]/td[1]"
race_going_xpath = "/html/body/div/div[4]/table/tbody/tr[2]/td[3]"
race_table_xpath = string.Template('''/html/body/div/div[5]/table/tbody/tr[$row]/td[$col]''')

total_meets = (len(driver.find_elements_by_tag_name('option')))

same_day_race_links = [
  "/html/body/div/div[2]/table/tbody/tr/td[3]/a",
  "/html/body/div/div[2]/table/tbody/tr/td[4]/a",
  "/html/body/div/div[2]/table/tbody/tr/td[5]/a",
  "/html/body/div/div[2]/table/tbody/tr/td[6]/a",
  "/html/body/div/div[2]/table/tbody/tr/td[7]/a",
  "/html/body/div/div[2]/table/tbody/tr/td[8]/a",
  "/html/body/div/div[2]/table/tbody/tr/td[9]/a",
  "/html/body/div/div[2]/table/tbody/tr/td[10]/a",
  "/html/body/div/div[2]/table/tbody/tr/td[11]/a"
]
all_race_entries = []


# Begin grabbing data
for same_day_link in same_day_race_links:
  driver.implicitly_wait(10)
  race_entries = []
  # Get one race - 12 columns 8 rows + race name, going, track type
  for row in range(1, 9):
    race_table_vals = list()
    race_table_vals.append(driver.find_element_by_xpath(race_name_xpath).text)
    race_table_vals.append(driver.find_element_by_xpath(race_going_xpath).text)
    race_table_vals.append(driver.find_element_by_xpath(race_type_xpath).text)
    for col in range(1, 13):
      rc = {'row': row, 'col': col}
      if (check_exists_by_xpath(race_table_xpath.substitute(rc))):
        race_table_vals.append(driver.find_element_by_xpath(race_table_xpath.substitute(rc)).text)
    race_entries.append(race_table_vals)
    race_table_vals = []

  print(race_entries)
  all_race_entries.append(race_entries)
  # Move on
  driver.find_element_by_xpath(same_day_link).click()

driver.quit()