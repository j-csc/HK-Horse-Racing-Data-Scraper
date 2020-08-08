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
#BASE_URL = "https://racing.hkjc.com/racing/information/chinese/Horse/Horse.aspx?HorseId=HK_2016_A310&Option=1"
BASE_URL = "https://racing.hkjc.com/racing/information/chinese/Horse/Horse.aspx?HorseId="
brandno = ["HK_2030_A001",
"HK_2000_A111",
"HK_2000_A278",
"HK_2001_B354",
"HK_2003_D078",
"HK_2003_D405",
"HK_2005_G108",
"HK_2006_H250",
"HK_2008_K358",
"HK_2009_L247",
"HK_2010_M220",
"HK_2012_P069",
"HK_2012_P180",
"HK_2013_S147",
"HK_2013_S235",
"HK_2013_S282",
"HK_2013_S391",
"HK_2014_T186",
"HK_2014_T245",
"HK_2014_T262",
"HK_2014_T349",
"HK_2014_T353",
"HK_2014_T390",
"HK_2015_V161",
"HK_2015_V337",
"HK_2015_V341",
"HK_2015_V357",
"HK_2015_V364",
"HK_2015_V368",
"HK_2015_V401",
"HK_2015_V407",
"HK_2016_A010",
"HK_2016_A022",
"HK_2016_A065",
"HK_2016_A086",
"HK_2016_A170",
"HK_2016_A190",
"HK_2016_A245",
"HK_2016_A251",
"HK_2016_A270",
"HK_2016_A293",
"HK_2016_A327",
"HK_2016_A371",
"HK_2016_A377",
"HK_2016_A379",
"HK_2016_A402",
"HK_2017_B067",
"HK_2017_B080",
"HK_2017_B095",
"HK_2017_B128",
"HK_2017_B169",
"HK_2017_B190",
"HK_2017_B192",
"HK_2017_B246",
"HK_2017_B251",
"HK_2017_B280",
"HK_2017_B285",
"HK_2017_B286",
"HK_2017_B288",
"HK_2017_B292",
"HK_2017_B311",
"HK_2017_B319",
"HK_2017_B349",
"HK_2017_B384",
"HK_2017_B403",
"HK_2017_B464",
"HK_2017_B473",
"HK_2018_C011",
"HK_2018_C027",
"HK_2018_C042",
"HK_2018_C058",
"HK_2018_C077",
"HK_2018_C102",
"HK_2018_C106",
"HK_2018_C123",
"HK_2018_C125",
"HK_2018_C126",
"HK_2018_C137",
"HK_2018_C141",
"HK_2018_C166",
"HK_2018_C193",
"HK_2018_C212",
"HK_2018_C234",
"HK_2018_C248",
"HK_2018_C251",
"HK_2018_C262",
"HK_2018_C275",
"HK_2018_C303",
"HK_2018_C326",
"HK_2018_C327",
"HK_2018_C334",
"HK_2018_C355",
"HK_2018_C357",
"HK_2018_C365",
"HK_2018_C417",
"HK_2018_C420",
"HK_2018_C434",
"HK_2018_C436",
"HK_2018_C451",
"HK_2018_C453",
"HK_2018_C458",
"HK_2018_C472",
"HK_2018_C473",
"HK_2018_C476",
"HK_2018_C504",
"HK_2018_C505",
"HK_2018_C508",
"HK_2018_C510",
"HK_2018_C512",
"HK_2018_C517",
"HK_2018_C519",
"HK_2018_C523",
"HK_2018_C527",
"HK_2018_C536",
"HK_2018_C540",
"HK_2019_D026",
"HK_2019_D027",
"HK_2019_D063",
"HK_2019_D067",
"HK_2019_D073",
"HK_2019_D075",
"HK_2019_D082",
"HK_2019_D099",
"HK_2019_D112",
"HK_2019_D115",
"HK_2019_D118",
"HK_2019_D122",
"HK_2019_D128",
"HK_2019_D136",
"HK_2019_D144",
"HK_2019_D154",
"HK_2019_D168",
"HK_2019_D169",
"HK_2019_D177",
"HK_2019_D200",
"HK_2019_D201",
"HK_2019_D206",
"HK_2019_D209",
"HK_2019_D210",
"HK_2019_D218",
"HK_2019_D219",
"HK_2019_D241",
"HK_2019_D266",
"HK_2019_D270",
"HK_2019_D271",
"HK_2019_D273",
"HK_2019_D279",
"HK_2019_D289",
"HK_2019_D298",
"HK_2019_D299",
"HK_2019_D322",
"HK_2019_D330",
"HK_2019_D344",
"HK_2019_D346",
"HK_2019_D361",
"HK_2019_D362",
"HK_2019_D363",
"HK_2019_D384",
"HK_2019_D391"


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
  
Racing Date, Racing No, Placing No, Horse Name, Jockey, Gear, Comment

"""
table_row_xpath =""
table_row_xpath = "//div/table[4]/tbody/tr"




Horse_Name_xpath ="/html/body/div/div/table[1]/tbody/tr/td[1]/table/tbody/tr[1]/td"


#/html/body/div/div[1]/table[3]/tbody/tr[3]/td[3]
#/html/body/div/div/table[3]/tbody/tr[4]/td[6]

#/html/body/div/div[1]/table[4]/tbody/tr[3]/td[3]
#/html/body/div/div/table[3]/tbody/tr[3]/td[4]
#/html/body/div/div/table[3]/tbody/tr[3]/td[5]
#/html/body/div/div[1]/table[3]/tbody/tr[4]/td[6]

#/html/body/div/div[1]/table[4]/tbody/tr[3]/td[6]

#/html/body/div/div[1]/table[2]/tbody/tr/td[3]/a

count = 0
horse_name =""

# Begin grabbing data
for horseid in brandno:
  print("Scraping: " + horseid)
  race_entry = []
  count += 1
  if os.path.isfile('Horse_Race_' + str(horseid) + '.txt'):
    continue
  else:
    driver.get(BASE_URL + horseid+"&Option=1")
    driver.implicitly_wait(5)



    # Get first race - x columns y rows + race name, going, track type
    #tempTableEl = wait.until(EC.presence_of_all_elements_located((By.XPATH, table_row_xpath)))
    #table_rows = tempTableEl



  if not (check_exists_by_xpath(Horse_Name_xpath)):
    continue
  else:

    if not (check_exists_by_xpath(table_row_xpath)):
      table_row_xpath = "//div/table[3]/tbody/tr"
      print ("3")
    else:
      table_row_xpath = "//div/table[4]/tbody/tr"
      print ("4")


  if not (check_exists_by_xpath(table_row_xpath)):
    continue
  else:
    tempTableEl = wait.until(EC.presence_of_all_elements_located((By.XPATH, table_row_xpath)))
    table_rows = tempTableEl

    if (check_exists_by_xpath(Horse_Name_xpath)):
      tempEl = wait.until(EC.presence_of_element_located((By.XPATH, Horse_Name_xpath)))
      horse_name = (tempEl.text)


    
    for row in table_rows:
      rowEntry = []

      rowEntry.append(horseid)
      rowEntry.append(horse_name)


      cols = row.find_elements_by_tag_name('td')
      for col in cols:
        rowEntry.append(col.text)

      race_entry.append(rowEntry)
      table_row_xpath =""
            
    # Save file as csv
    df = pd.DataFrame(race_entry)
    print(df.head())
    csv_data = df.to_csv("./Horse_Race_" + str(horseid) + ".txt", index=False)
    print("Saved " + str(horseid))

driver.quit()
