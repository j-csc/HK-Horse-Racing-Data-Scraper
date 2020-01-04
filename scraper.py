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

#starting webdriver
BASE_URL = "https://racing.hkjc.com/racing/information/English/racing/LocalResults.aspx?RaceDate="
dates = ["29/12/2019", "26/12/2019", "21/12/2019", "18/12/2019", "15/12/2019", "11/12/2019", "08/12/2019",
 "04/12/2019", "01/12/2019", "27/11/2019", "23/11/2019", "20/11/2019", "17/11/2019", "13/11/2019", "09/11/2019",
  "06/11/2019", "03/11/2019", "30/10/2019", "27/10/2019", "23/10/2019", "20/10/2019", "16/10/2019",
   "12/10/2019", "09/10/2019", "01/10/2019", "25/09/2019", "21/09/2019", "15/09/2019", "11/09/2019",
     "01/09/2019", "14/07/2019", "10/07/2019", "07/07/2019", "03/07/2019", "01/07/2019", "26/06/2019", "23/06/2019",
      "16/06/2019", "05/06/2019", "29/05/2019", "22/05/2019", "15/05/2019", "11/05/2019", "08/05/2019", "05/05/2019",
       "01/05/2019", "28/04/2019", "22/04/2019",  "07/04/2019","03/04/2019", "31/03/2019", "24/03/2019", "23/03/2019", "20/03/2019",
        "17/03/2019", "13/03/2019", "10/03/2019", "06/03/2019", "02/03/2019", "27/02/2019",
         "24/02/2019", "17/02/2019", "13/02/2019","10/02/2019", "07/02/2019", "02/02/2019", "30/01/2019", "27/01/2019",
          "23/01/2019", "20/01/2019", "16/01/2019", "12/01/2019", "09/01/2019", "06/01/2019", "01/01/2019",
           "29/12/2018", "26/12/2018", "23/12/2018", "19/12/2018", "16/12/2018", "12/12/2018", "09/12/2018",
            "05/12/2018", "02/12/2018", "28/11/2018", "25/11/2018", "21/11/2018", "18/11/2018", "14/11/2018", "10/11/2018", "07/11/2018",
             "04/11/2018", "31/10/2018", "28/10/2018", "24/10/2018", "21/10/2018",  "18/10/2018",
              "13/10/2018", "10/10/2018", "01/10/2018", "26/09/2018", "22/09/2018", "12/09/2018",
               "09/09/2018", "05/09/2018", "02/09/2018"]
 
driver = webdriver.Firefox()
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
  place, horse_no, horse, jockey, trainer, actual_wt,
  declare_horse_wt, draw, lbw, running_pos, finish_time, win_odds
"""

race_name_xpath = "/html/body/div/div[4]/table/thead/tr/td[1]"
race_type_xpath = "/html/body/div/div[4]/table/tbody/tr[2]/td[1]"
race_going_xpath = "/html/body/div/div[4]/table/tbody/tr[2]/td[3]"
race_table_xpath = string.Template('''/html/body/div/div[5]/table/tbody/tr[$row]/td[$col]''')

same_day_race_link_xpaths = "//div[2]/table/tbody/tr/td/a"
table_row_xpath = "//div[5]/table/tbody/tr"

count = 0

# Begin grabbing data
for meet in dates:
  print("Scraping: " + meet)
  all_race_entries = []
  count += 1
  if os.path.isfile('races' + str(count) + '.csv'):
    continue
  else:
    driver.get(BASE_URL + meet)
    driver.implicitly_wait(20)
    same_day_selel = driver.find_elements_by_xpath(same_day_race_link_xpaths)[:-1]
    same_day_links = [x.get_attribute("href") for x in same_day_selel]  
    
    # Get first race - x columns y rows + race name, going, track type
    tempTableEl = wait.until(EC.presence_of_all_elements_located((By.XPATH, table_row_xpath)))
    table_rows = tempTableEl
    first_race_entry = []

    if (check_exists_by_xpath(race_name_xpath)):
      tempEl = wait.until(EC.presence_of_element_located((By.XPATH, race_name_xpath)))
      first_race_entry.append(tempEl.text)
    if (check_exists_by_xpath(race_going_xpath)):
      tempEl = wait.until(EC.presence_of_element_located((By.XPATH,race_going_xpath)))
      first_race_entry.append(tempEl.text)
    if (check_exists_by_xpath(race_type_xpath)):
      tempEl = wait.until(EC.presence_of_element_located((By.XPATH,race_type_xpath)))
      first_race_entry.append(tempEl.text)
    print(first_race_entry)
    for row in table_rows:
      cols = row.find_elements_by_tag_name('td')
      for col in cols:
        first_race_entry.append(col.text)
    all_race_entries.append(first_race_entry)
    
    # Get other races on same meet
    for same_day_link in same_day_links:
      print("Scraping " + same_day_link)
      driver.get(same_day_link)
      driver.implicitly_wait(10)

      # Scrape 2nd - n
      race_entry = []
      if (check_exists_by_xpath(race_name_xpath)):
        tempEl = wait.until(EC.presence_of_element_located((By.XPATH, race_name_xpath)))
        race_entry.append(tempEl.text)
      if (check_exists_by_xpath(race_going_xpath)):
        tempEl = wait.until(EC.presence_of_element_located((By.XPATH,race_going_xpath)))
        race_entry.append(tempEl.text)
      if (check_exists_by_xpath(race_type_xpath)):
        tempEl = wait.until(EC.presence_of_element_located((By.XPATH,race_type_xpath)))
        race_entry.append(tempEl.text)

      print(race_entry)

      table_rows = driver.find_elements_by_xpath(table_row_xpath)
      for row in table_rows:
        cols = row.find_elements_by_tag_name('td')
        for col in cols:
          race_entry.append(col.text)
      all_race_entries.append(race_entry)

    # Save file as csv
    df = pd.DataFrame(all_race_entries)
    df.head()
    csv_data = df.to_csv("./races" + str(count) + ".csv", index=False)
    print("Saved " + str(count))

driver.quit()