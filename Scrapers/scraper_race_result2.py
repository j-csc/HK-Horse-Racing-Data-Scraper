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
BASE_URL = "https://racing.hkjc.com/racing/information/english/Racing/Fixture.aspx?CalYear="
#dates = ["2020-06-07","2020-06-03"]
dates=[
"2020&CalMonth=09",
"2020&CalMonth=10",
"2020&CalMonth=11",
"2020&CalMonth=12",



]
 
#driver = webdriver.Firefox()
#driver = webdriver.Chrome(r"C:\chromedriver")
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
  Racing Date, Racing Number,
  place, horse_no, horse, jockey, trainer, actual_wt,
  declare_horse_wt, draw, lbw, running_pos, finish_time, win_odds
"""

race_name_xpath = "/html/body/div/div[4]/table/thead/tr/td[1]"



race_table_xpath = string.Template('''/html/body/div/div[5]/table/tbody/tr[$row]/td[$col]''')

same_day_race_link_xpaths = "//div[@class='f_clear f_tac f_fs13']/div[2]/ul/li/a"
#/html/body/div/div[2]/ul/li[6]/a
#/html/body/div/div[2]/ul/li[10]/a
#/html/body/div/div[2]/ul
#/div[@class='f_clear f_tac f_fs13']/div/div[2]/ul/li/a
table_row_xpath = "//div/div[3]/table/tbody/tr"

#/html/body/div/div[3]/table/tbody/tr[2]/td[4]/p[1]


count = 0
race_name = ""


# Begin grabbing data
for meet in dates:
  print("Scraping: ")
  race_entry = []
  internalRaceCount = 1
  count += 1
  if os.path.isfile('Fixture_' + str(meet)+'.txt'):
    continue
  else:
      driver.get(BASE_URL + meet)
      driver.implicitly_wait(20)
      same_day_selel = driver.find_elements_by_xpath(same_day_race_link_xpaths)[:-1]
      same_day_links = [x.get_attribute("href") for x in same_day_selel]  

      # Get first race - x columns y rows + race name, going, track type
      #tempTableEl = wait.until(EC.presence_of_all_elements_located((By.XPATH, table_row_xpath)))
      #table_rows = tempTableEl

      if not (check_exists_by_xpath(table_row_xpath)):
        print("Not Found")
        continue
      else:
        tempTableEl = wait.until(EC.presence_of_all_elements_located((By.XPATH, table_row_xpath)))
        table_rows = tempTableEl

      #if (check_exists_by_xpath(race_name_xpath)):
        #tempEl = wait.until(EC.presence_of_element_located((By.XPATH, race_name_xpath)))
        #race_name = (tempEl.text)



        
        
      for row in table_rows:
        rowEntry = []

        #rowEntry.append(meet)

        #rowEntry.append(race_name)


        cols = row.find_elements_by_tag_name('td')
        for col in cols:
          rowEntry.append(col.text)
        race_entry.append(rowEntry)
      


          
      # Save file as csv
      df = pd.DataFrame(race_entry)
      print(df.head())
      csv_data = df.to_csv("./Fixture_" + str(meet)+ ".txt", index=False)
      print("Saved " + str(meet))

driver.quit()
