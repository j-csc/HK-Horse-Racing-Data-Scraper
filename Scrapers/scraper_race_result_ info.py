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
BASE_URL = "https://racing.hkjc.com/racing/information/Chinese/racing/LocalResults.aspx?RaceDate="
dates = [ 
"1970-07-01",

"2020-07-15"

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
Racing Date, Racing Number, Race Name, Race Type, Race Going,
RaceHandicap, RaceStake, Race Course,
Race Sect1, Race Sect2, Race Sect3, Race Sect4, Race Sect5, Race Sect6
"""

race_name_xpath = "/html/body/div/div[4]/table/thead/tr/td[1]"
race_type_xpath = "/html/body/div/div[4]/table/tbody/tr[2]/td[1]"
race_going_xpath = "/html/body/div/div[4]/table/tbody/tr[2]/td[3]"
race_CupName_xpath = "/html/body/div/div[4]/table/tbody/tr[3]/td[1]"
race_Stake_xpath = "/html/body/div/div[4]/table/tbody/tr[4]/td[1]"
race_Course_xpath = "/html/body/div/div[4]/table/tbody/tr[3]/td[3]"
race_Sect1_xpath = "/html/body/div/div[4]/table/tbody/tr[5]/td[3]"
race_Sect2_xpath = "/html/body/div/div[4]/table/tbody/tr[5]/td[4]"
race_Sect3_xpath = "/html/body/div/div[4]/table/tbody/tr[5]/td[5]"
race_Sect4_xpath = "/html/body/div/div[4]/table/tbody/tr[5]/td[6]"
race_Sect5_xpath = "/html/body/div/div[4]/table/tbody/tr[5]/td[7]"
race_Sect6_xpath = "/html/body/div/div[4]/table/tbody/tr[5]/td[8]"


race_table_xpath = string.Template('''/html/body/div/div[5]/table/tbody/tr[$row]/td[$col]''')

same_day_race_link_xpaths = "//div[2]/table/tbody/tr/td/a"
table_row_xpath = "//div[5]/table/tbody/tr"

count = 0
race_name = ""
race_going = ""
race_type = ""
race_CupName = ""
race_Stake = ""
race_Course = ""
race_Sect1 = ""
race_Sect2 = ""
race_Sect3 = ""
race_Sect4 = ""
race_Sect5 = ""
race_Sect6 = ""

# Begin grabbing data
for meet in dates:
  print("Scraping: " + meet)
  race_entry = []
  internalRaceCount = 1
  count += 1
  if os.path.isfile('Races_Result_Info_' + str(meet) + '.txt'):
    continue
  else:
    driver.get(BASE_URL + meet)
    driver.implicitly_wait(10)
    same_day_selel = driver.find_elements_by_xpath(same_day_race_link_xpaths)[:-1]
    same_day_links = [x.get_attribute("href") for x in same_day_selel]  
    
  # Get first race - x columns y rows + race name, going, track type
    #tempTableEl = wait.until(EC.presence_of_all_elements_located((By.XPATH, table_row_xpath)))
    #table_rows = tempTableEl

  if not (check_exists_by_xpath(table_row_xpath)):
    continue
  else:
    tempTableEl = wait.until(EC.presence_of_all_elements_located((By.XPATH, table_row_xpath)))
    table_rows = tempTableEl

  if (check_exists_by_xpath(race_name_xpath)):
    tempEl = wait.until(EC.presence_of_element_located((By.XPATH, race_name_xpath)))
    race_name = (tempEl.text)
  if (check_exists_by_xpath(race_going_xpath)):
    tempEl = wait.until(EC.presence_of_element_located((By.XPATH,race_going_xpath)))
    race_going = (tempEl.text)
  if (check_exists_by_xpath(race_type_xpath)):
    tempEl = wait.until(EC.presence_of_element_located((By.XPATH,race_type_xpath)))
    race_type = (tempEl.text)
  if (check_exists_by_xpath(race_Course_xpath)):
    tempEl = wait.until(EC.presence_of_element_located((By.XPATH,race_Course_xpath)))
    race_Course = (tempEl.text)
  if (check_exists_by_xpath(race_CupName_xpath)):
    tempEl = wait.until(EC.presence_of_element_located((By.XPATH,race_CupName_xpath)))
    race_CupName = (tempEl.text)    
  if (check_exists_by_xpath(race_Stake_xpath)):
    tempEl = wait.until(EC.presence_of_element_located((By.XPATH,race_Stake_xpath)))
    race_Stake = (tempEl.text) 
  if (check_exists_by_xpath(race_Sect1_xpath)):
    tempEl = wait.until(EC.presence_of_element_located((By.XPATH,race_Sect1_xpath)))
    race_Sect1 = (tempEl.text)
  if (check_exists_by_xpath(race_Sect2_xpath)):
    tempEl = wait.until(EC.presence_of_element_located((By.XPATH,race_Sect2_xpath)))
    race_Sect2 = (tempEl.text)
  if (check_exists_by_xpath(race_Sect3_xpath)):
    tempEl = wait.until(EC.presence_of_element_located((By.XPATH,race_Sect3_xpath)))
    race_Sect3 = (tempEl.text)   
  if (check_exists_by_xpath(race_Sect4_xpath)):
    tempEl = wait.until(EC.presence_of_element_located((By.XPATH,race_Sect4_xpath)))
    race_Sect4 = (tempEl.text)
  if (check_exists_by_xpath(race_Sect5_xpath)):
    tempEl = wait.until(EC.presence_of_element_located((By.XPATH,race_Sect5_xpath)))
    race_Sect5 = (tempEl.text)
  if (check_exists_by_xpath(race_Sect6_xpath)):
    tempEl = wait.until(EC.presence_of_element_located((By.XPATH,race_Sect6_xpath)))
    race_Sect6 = (tempEl.text)




    
    
#for row in table_rows:
  rowEntry = []

  rowEntry.append(meet)

  rowEntry.append(race_name)
  rowEntry.append(race_going)
  rowEntry.append(race_type)

  rowEntry.append(race_CupName)
  rowEntry.append(race_Stake)
  rowEntry.append(race_Course)
  rowEntry.append(race_Sect1)
  rowEntry.append(race_Sect2)
  rowEntry.append(race_Sect3)
  rowEntry.append(race_Sect4)
  rowEntry.append(race_Sect5)
  rowEntry.append(race_Sect6) 

  #cols = row.find_elements_by_tag_name('td')
  #for col in cols:
    #rowEntry.append(col.text)
  race_entry.append(rowEntry)


         
    
  # Get other races on same meet
  for same_day_link in same_day_links:
    print("Scraping " + same_day_link)
    internalRaceCount += 1
    driver.get(same_day_link)
    driver.implicitly_wait(5)

    race_name = ""
    race_going = ""
    race_type = ""
    race_CupName = ""
    race_Stake = ""
    race_Course = ""
    race_Sect1 = ""
    race_Sect2 = ""
    race_Sect3 = ""
    race_Sect4 = ""
    race_Sect5 = ""
    race_Sect6 = ""

    # Scrape 2nd - n
    if (check_exists_by_xpath(race_name_xpath)):
      tempEl = wait.until(EC.presence_of_element_located((By.XPATH, race_name_xpath)))
      race_name = (tempEl.text)
    if (check_exists_by_xpath(race_going_xpath)):
      tempEl = wait.until(EC.presence_of_element_located((By.XPATH,race_going_xpath)))
      race_going = (tempEl.text)
    if (check_exists_by_xpath(race_type_xpath)):
      tempEl = wait.until(EC.presence_of_element_located((By.XPATH,race_type_xpath)))
      race_type = (tempEl.text)
    if (check_exists_by_xpath(race_Course_xpath)):
      tempEl = wait.until(EC.presence_of_element_located((By.XPATH,race_Course_xpath)))
      race_Course = (tempEl.text)
    if (check_exists_by_xpath(race_CupName_xpath)):
      tempEl = wait.until(EC.presence_of_element_located((By.XPATH,race_CupName_xpath)))
      race_CupName = (tempEl.text)
    if (check_exists_by_xpath(race_Stake_xpath)):
      tempEl = wait.until(EC.presence_of_element_located((By.XPATH,race_Stake_xpath)))
      race_Stake = (tempEl.text)
    if (check_exists_by_xpath(race_Sect1_xpath)):
      tempEl = wait.until(EC.presence_of_element_located((By.XPATH,race_Sect1_xpath)))
      race_Sect1 = (tempEl.text)
    if (check_exists_by_xpath(race_Sect2_xpath)):
      tempEl = wait.until(EC.presence_of_element_located((By.XPATH,race_Sect2_xpath)))
      race_Sect2 = (tempEl.text)
    if (check_exists_by_xpath(race_Sect3_xpath)):
      tempEl = wait.until(EC.presence_of_element_located((By.XPATH,race_Sect3_xpath)))
      race_Sect3 = (tempEl.text)   
    if (check_exists_by_xpath(race_Sect4_xpath)):
      tempEl = wait.until(EC.presence_of_element_located((By.XPATH,race_Sect4_xpath)))
      race_Sect4 = (tempEl.text)
    if (check_exists_by_xpath(race_Sect5_xpath)):
      tempEl = wait.until(EC.presence_of_element_located((By.XPATH,race_Sect5_xpath)))
      race_Sect5 = (tempEl.text)
    if (check_exists_by_xpath(race_Sect6_xpath)):
      tempEl = wait.until(EC.presence_of_element_located((By.XPATH,race_Sect6_xpath)))
      race_Sect6 = (tempEl.text)        
    
    #table_rows = driver.find_elements_by_xpath(table_row_xpath)

    #for row in table_rows:
    rowEntry = []

    rowEntry.append(meet)
    
    rowEntry.append(race_name)
    rowEntry.append(race_going)
    rowEntry.append(race_type)

    rowEntry.append(race_CupName)
    rowEntry.append(race_Stake)
    rowEntry.append(race_Course)
    rowEntry.append(race_Sect1)
    rowEntry.append(race_Sect2)
    rowEntry.append(race_Sect3)
    rowEntry.append(race_Sect4)
    rowEntry.append(race_Sect5)
    rowEntry.append(race_Sect6) 
      
      #cols = row.find_elements_by_tag_name('td')
      #for col in cols:
        #rowEntry.append(col.text)
    race_entry.append(rowEntry)
        
  # Save file as csv
  df = pd.DataFrame(race_entry)
  print(df.head())
  csv_data = df.to_csv("./Races_Result_Info_" + str(meet) + ".txt", index=False)
  print("Saved " + str(meet))

driver.quit()
