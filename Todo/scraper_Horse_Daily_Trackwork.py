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
BASE_URL = "https://racing.hkjc.com/racing/information/chinese/Trackwork/TrackworkOneDayResult.aspx?OneDay="
dates = ["01/07/2030",

"31/07/2020",         
"01/08/2020",
"02/08/2020",
"03/08/2020",        
"04/08/2020",
"05/08/2020",





]
 

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
Date, Horse, Trainer, Type, Racecourse/Track, Workouts, Gear
"""
table_row_xpath = "/html/body/div/div[3]/table/tbody/tr"

count = 0

# Begin grabbing data
for meet in dates:
  print("Scraping: " + meet)
  race_entry = []
  internalRaceCount = 1
  count += 1
  if os.path.isfile('Daily_Trackwork_' + str(meet.replace('/', '-')) + '.txt'):
    continue
  else:
    driver.get(BASE_URL + meet)
    driver.implicitly_wait(20)

  # Get BrandNo, Date, Type, Racecourse/Track, Workouts, Gear
  
  #if (check_exists_by_xpath(table_row_xpath)):
    #tempTableEl = wait.until(EC.presence_of_all_elements_located((By.XPATH, table_row_xpath)))
    #table_rows = tempTableEl

  if not (check_exists_by_xpath(table_row_xpath)):
    continue
  else:
    tempTableEl = wait.until(EC.presence_of_all_elements_located((By.XPATH, table_row_xpath)))
    table_rows = tempTableEl

    for row in table_rows:
      rowEntry = []

      rowEntry.append(meet)
 
      cols = row.find_elements_by_tag_name('td')
      for col in cols:
        rowEntry.append(col.text)
      race_entry.append(rowEntry)
     
    # Save file as csv
    df = pd.DataFrame(race_entry)
    print(df.head())
    csv_data = df.to_csv("./Daily_Trackwork_" + str(meet.replace('/', '-')) + ".txt", index=False)
    #csv_data = df.to_csv("./Daily_Trackwork_" + str(meet) + ".csv", index=False)
    print("Saved " + str(meet))

driver.quit()
