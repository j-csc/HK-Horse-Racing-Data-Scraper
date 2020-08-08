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

BASE_URL = "https://racing.hkjc.com/racing/Info/meeting/RaceCard/chinese/Local/"
 

"""
Initialize variables: 

Data collected per entry: 
Racing Date, Racing Name, Horse No., Last 6 Runs, Colour, Horse, Brand No, Wt, Draw, Over Wt, Jockey, Trainer, Rtg, Rtg.+/-, Horse Wt. (Declaration), Wt.+/- (vs Declaration), Best Time, Age, WFA, Sex, Season Stakes, Priority, Gear, Owner, Sire, Dam, Import Cat.
"""

def scrape_racecard_info(dates):
  driver = webdriver.Firefox()

  wait = WebDriverWait(driver, 20)

  def check_exists_by_xpath(xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True

  same_day_race_link_xpaths = "/html/body/div/div[3]/table/tbody/tr/td/a"

  table_row_xpath = "//div[7]/table/tbody/tr/td/table/tbody/tr"
  racecard_info_1_xpath = "/html/body/div/div[4]/div[2]"
  #racecard_info_2_xpath = "/html/body/div/div[4]/div[2]/text()[2]"


  count = 0
  race_name = 1
  racecard_info_1 = ""
  #racecard_info_2 = ""

  # Begin grabbing data
  for meet in dates:
    print("Scraping: " + meet)
    race_entry = []
    internalRaceCount = 1
    count += 1
    if os.path.isfile('Racescard_Info_' + str(meet) + '.txt'):
      continue
    else:
      driver.get(BASE_URL + meet.replace('-',''))
      driver.implicitly_wait(20)
      #same_day_selel = driver.find_elements_by_xpath(same_day_race_link_xpaths)[:-1]
      same_day_selel = driver.find_elements_by_xpath(same_day_race_link_xpaths)
      same_day_links = [x.get_attribute("href") for x in same_day_selel]  
      #race_name=driver.findAll("div",{'class':"raceInfo"})
      
    # Get first race - x columns y rows + race name, going, track type
    #if not (check_exists_by_xpath(table_row_xpath)):
    if not (check_exists_by_xpath(racecard_info_1_xpath)):
      continue
    else:
      #tempTableEl = wait.until(EC.presence_of_all_elements_located((By.XPATH, table_row_xpath)))
      #table_rows = tempTableEl
      tempEl = wait.until(EC.presence_of_element_located((By.XPATH, racecard_info_1_xpath)))
      racecard_info_1 = (tempEl.text)
    
    rowEntry = []
    rowEntry.append(meet)
    rowEntry.append(racecard_info_1)
    race_entry.append(rowEntry)
          
    # Get other races on same meet
    for same_day_link in same_day_links:
      print("Scraping " + same_day_link)
      internalRaceCount += 1
      driver.get(same_day_link)
      driver.implicitly_wait(10)

      racecard_info_1 = ""


      # Scrape 2nd - n
      #if not (check_exists_by_xpath(table_row_xpath)):
      if not (check_exists_by_xpath(racecard_info_1_xpath)):  
        continue
      else:
        #tempTableEl = wait.until(EC.presence_of_all_elements_located((By.XPATH, table_row_xpath)))
        #table_rows = tempTableEl
        tempEl = wait.until(EC.presence_of_element_located((By.XPATH, racecard_info_1_xpath)))
        racecard_info_1 = (tempEl.text)

      rowEntry = []

      rowEntry.append(meet)
      rowEntry.append(racecard_info_1)
      #rowEntry.append(racecard_info_2)
      race_entry.append(rowEntry)
   
    # Save file as csv
    df = pd.DataFrame(race_entry)
    print(df.head())
    csv_data = df.to_csv("./Racescard_Info_" + str(meet) + ".txt", index=False)
    print("Saved " + str(meet))

  driver.quit()
