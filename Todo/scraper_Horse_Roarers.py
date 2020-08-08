#import libraries
from bs4 import BeautifulSoup
import requests
import string
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
import pandas as pd
import os.path
import re

#starting webdriver
BASE_URL = "https://racing.hkjc.com/racing/information/Chinese/VeterinaryRecords/OveRoar.aspx"
 
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)

def check_exists_by_xpath(xpath):
  try:
      driver.find_element_by_xpath(xpath)
  except NoSuchElementException:
      return False
  return True

"""
Initialize variables: 

Data collected per entry: 
Brand No., Horse Name, Date, Surgery
"""

race_table_xpath = string.Template('''/html/body/div/table/tbody/tr[$row]/td[$col]''')
table_row_xpath = "//div/table/tbody/tr"


race_meet_xpath="/html/body/div/table/thead/tr[1]/td"


count = 0
race_meet = "2020-07-24"

# Begin grabbing data

race_entry = []
internalRaceCount = 1
count += 1


driver.get(BASE_URL)
driver.implicitly_wait(20)

tempTableEl = wait.until(EC.presence_of_all_elements_located((By.XPATH, table_row_xpath)))
table_rows = tempTableEl

if (check_exists_by_xpath(race_meet_xpath)):
  tempEl = wait.until(EC.presence_of_element_located((By.XPATH,race_meet_xpath)))
  race_meet = (tempEl.text)

if not os.path.isfile('Horse_Roarers_' + str(race_meet) + '.txt'):
  print("Scraping: " +  race_meet)

  for row in table_rows:
    rowEntry = []


    cols = row.find_elements_by_tag_name('td')
    for col in cols:
      rowEntry.append(col.text)
    race_entry.append(rowEntry)

  # Save file as csv

  #df = pd.DataFrame(race_entry)
  df = pd.DataFrame(race_entry)
  print(df.head())
  csv_data = df.to_csv("./Horse_Roarers_" + str(race_meet) + ".txt", index=False)
  print("Saved " + str(race_meet))



driver.quit()

