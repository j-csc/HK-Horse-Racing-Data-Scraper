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
BASE_URL = "https://racing.hkjc.com/racing/Info/meeting/RaceCard/chinese/Local/"

"""
Initialize variables: 

Data collected per entry: 
Racing Date, Racing Name, Horse No., Last 6 Runs, Colour, Horse, Brand No, Wt, Draw, 
Over Wt, Jockey, Trainer, Rtg, Rtg.+/-, Horse Wt. (Declaration), Wt.+/- (vs Declaration), 
Best Time, Age, WFA, Sex, Season Stakes, Priority, Gear, Owner, Sire, Dam, Import Cat.

"""

def scrape_racecard(dates):

  driver = webdriver.Firefox()

  wait = WebDriverWait(driver, 20)

  def check_exists_by_xpath(xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True

  same_day_race_link_xpaths = "//div[3]/table/tbody/tr/td/a"
  same_day_race_link_xpaths = "/html/body/div/div[3]/table/tbody/tr/td/a"
  table_row_xpath = "//div[7]/table/tbody/tr/td/table/tbody/tr"
  reserve_table_row_xpath ="//div[8]/table/tbody/tr"
  racecard_info_1_xpath = "/html/body/div/div[4]/div[2]"

  count = 0
  race_name = 1

  # Begin grabbing data
  for meet in dates:
    print("Scraping: " + meet)
    race_entry = []
    reserverace_entry = []
    race_standby = []
    internalRaceCount = 1
    count += 1
    if os.path.isfile('Racescard_' + str(meet) + '.txt'):
      continue
    else:
      driver.get(BASE_URL + meet.replace('-',''))
      driver.implicitly_wait(20)
      same_day_selel = driver.find_elements_by_xpath(same_day_race_link_xpaths)
      same_day_links = [x.get_attribute("href") for x in same_day_selel]  

      # Get first race - x columns y rows + race name, going, track type
      if not (check_exists_by_xpath(racecard_info_1_xpath)):
        continue
      else:
        if not (check_exists_by_xpath(table_row_xpath)):
          rowEntry = []
          rowEntry.append(meet)
          rowEntry.append(race_name)
          race_entry.append(rowEntry)
        else:
          tempTableEl = wait.until(EC.presence_of_all_elements_located((By.XPATH, table_row_xpath)))
          table_rows = tempTableEl

        if (check_exists_by_xpath(reserve_table_row_xpath)):
          tempTableEl2 = wait.until(EC.presence_of_all_elements_located((By.XPATH, reserve_table_row_xpath)))
          reserve_table_rows = tempTableEl2
          
          race_name = 1
          race_standby = "正選"
          for row in table_rows:
            rowEntry = []
            rowEntry.append(meet)
            rowEntry.append(race_name)
            rowEntry.append(race_standby) 
            cols = row.find_elements_by_tag_name('td')
            for col in cols:
              rowEntry.append(col.text)
            race_entry.append(rowEntry)

          race_standby = "後備"
          for reserverow in reserve_table_rows:
            reserverowEntry = []
            reserverowEntry.append(meet)
            reserverowEntry.append(race_name)
            reserverowEntry.append(race_standby) 
            reservecols = reserverow.find_elements_by_tag_name('td')
            for reservecol in reservecols:
              reserverowEntry.append(reservecol.text)
            race_entry.append(reserverowEntry)
                    
        # # Get other races on same meet
        # for same_day_link in same_day_links:
        #   print("Scraping " + same_day_link)
        #   internalRaceCount += 1
        #   driver.get(same_day_link)
        #   driver.implicitly_wait(10)

        #   # Scrape 2nd - n
        #   #if not (check_exists_by_xpath(table_row_xpath)):
        #   if not (check_exists_by_xpath(racecard_info_1_xpath)):  
        #     continue
        #   else:
        #     #tempTableEl = wait.until(EC.presence_of_all_elements_located((By.XPATH, table_row_xpath)))
        #     #table_rows = tempTableEl

        #     #if (check_exists_by_xpath(race_name_xpath)):
        #       #tempEl = wait.until(EC.presence_of_element_located((By.XPATH, race_name_xpath)))
        #       #race_name = (tempEl.text)
        #     if not (check_exists_by_xpath(table_row_xpath)):
        #       rowEntry = []
        #       rowEntry.append(meet)
        #       rowEntry.append(race_name)
        #       race_entry.append(rowEntry)
        #     else:   
        #       #tempEl2 = wait.until(EC.presence_of_element_located((By.XPATH, reserve_table_row_xpath)))
        #       #reserve_table_rows = tempEl2
        #       tempTableEl = wait.until(EC.presence_of_all_elements_located((By.XPATH, table_row_xpath)))
        #       table_rows = tempTableEl
        #     #if (check_exists_by_xpath(race_name_xpath)):
        #       #tempEl = wait.until(EC.presence_of_element_located((By.XPATH, race_name_xpath)))
        #       #race_name = (tempEl.text)
        #     if (check_exists_by_xpath(reserve_table_row_xpath)):
        #       #tempEl2 = wait.until(EC.presence_of_element_located((By.XPATH, reserve_table_row_xpath)))
        #       #reserve_table_rows = tempEl2
        #       tempTableEl2 = wait.until(EC.presence_of_all_elements_located((By.XPATH, reserve_table_row_xpath)))
        #       reserve_table_rows = tempTableEl2


            
        #     table_rows = driver.find_elements_by_xpath(table_row_xpath)
        #     race_name += 1
        #     race_standby = "正選"
        #     for row in table_rows:
        #       rowEntry = []

        #       rowEntry.append(meet)

        #       rowEntry.append(race_name)
        #       rowEntry.append(race_standby) 

              
        #       cols = row.find_elements_by_tag_name('td')
        #       for col in cols:
        #         rowEntry.append(col.text)
        #       race_entry.append(rowEntry)

        #     reserve_table_rows = driver.find_elements_by_xpath(reserve_table_row_xpath)
        #     race_standby = "後備"
        #     for reserverow in reserve_table_rows:
        #       reserverowEntry = []
        #       reserverowEntry.append(meet)
        #       reserverowEntry.append(race_name)
        #       reserverowEntry.append(race_standby) 
        #       reservecols = reserverow.find_elements_by_tag_name('td')
        #       for reservecol in reservecols:
        #         reserverowEntry.append(reservecol.text)
        #       race_entry.append(reserverowEntry)
            
        # # Save file as csv
        # df = pd.DataFrame(race_entry)
        # print(df.head())
        # csv_data = df.to_csv("./Racescard_" + str(meet) + ".txt", index=False)
        # print("Saved " + str(meet))

  driver.quit()
