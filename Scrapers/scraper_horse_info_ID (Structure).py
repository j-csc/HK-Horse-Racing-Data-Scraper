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

"HK_1979_N009",
"HK_1979_N008",
"HK_1979_N007",
"HK_1979_N006",
"HK_1979_N005",
"HK_1979_N004",
"HK_1979_N003",
"HK_1979_N002",
"HK_1979_N001",
"HK_1978_M239",
"HK_1978_M237",
"HK_1978_M236",
"HK_1978_M234",
"HK_1978_M233",
"HK_1978_M232",
"HK_1978_M231",
"HK_1978_M230",
"HK_1978_M229",
"HK_1978_M228",
"HK_1978_M227",
"HK_1978_M226",
"HK_1978_M225",
"HK_1978_M224",
"HK_1978_M223",
"HK_1978_M222",
"HK_1978_M221",
"HK_1978_M220",
"HK_1978_M219",
"HK_1978_M216",
"HK_1978_M215",
"HK_1978_M214",
"HK_1978_M213",
"HK_1978_M212",
"HK_1978_M211",
"HK_1978_M210",
"HK_1978_M209",
"HK_1978_M208",
"HK_1978_M207",
"HK_1978_M206",
"HK_1978_M205",
"HK_1978_M204",
"HK_1978_M203",
"HK_1978_M202",
"HK_1978_M201",
"HK_1978_M200",
"HK_1978_M199",
"HK_1978_M198",
"HK_1978_M197",
"HK_1978_M196",
"HK_1978_M195",
"HK_1978_M194",
"HK_1978_M193",
"HK_1978_M192",
"HK_1978_M191",
"HK_1978_M190",
"HK_1978_M189",
"HK_1978_M188",
"HK_1978_M187",
"HK_1978_M186",
"HK_1978_M185",
"HK_1978_M184",
"HK_1978_M183",
"HK_1978_M182",
"HK_1978_M181",
"HK_1978_M180",
"HK_1978_M179",
"HK_1978_M178",
"HK_1978_M177",
"HK_1978_M174",
"HK_1978_M173",
"HK_1978_M172",
"HK_1978_M169",
"HK_1978_M168",
"HK_1978_M167",
"HK_1978_M166",
"HK_1978_M161",
"HK_1978_M160",
"HK_1978_M159",
"HK_1978_M156",
"HK_1978_M155",
"HK_1978_M152",
"HK_1978_M151",
"HK_1978_M150",
"HK_1978_M149",
"HK_1978_M148",
"HK_1978_M147",
"HK_1978_M146",
"HK_1978_M145",
"HK_1978_M144",
"HK_1978_M143",
"HK_1978_M142",
"HK_1978_M141",
"HK_1978_M140",
"HK_1978_M139",
"HK_1978_M138",
"HK_1978_M137",
"HK_1978_M136",
"HK_1978_M135",
"HK_1978_M134",
"HK_1978_M133",
"HK_1978_M132",
"HK_1978_M131",
"HK_1978_M130",
"HK_1978_M129",
"HK_1978_M126",
"HK_1978_M125",
"HK_1978_M124",
"HK_1978_M123",
"HK_1978_M122",
"HK_1978_M121",
"HK_1978_M120",
"HK_1978_M119",
"HK_1978_M118",
"HK_1978_M117",
"HK_1978_M116",
"HK_1978_M115",
"HK_1978_M114",
"HK_1978_M113",
"HK_1978_M110",
"HK_1978_M109",
"HK_1978_M106",
"HK_1978_M105",
"HK_1978_M104",
"HK_1978_M103",
"HK_1978_M102",
"HK_1978_M101",
"HK_1978_M100",
"HK_1978_M096",
"HK_1978_M095",
"HK_1978_M092",
"HK_1978_M091",
"HK_1978_M090",
"HK_1978_M086",
"HK_1978_M085",
"HK_1978_M082",
"HK_1978_M081",
"HK_1978_M080",
"HK_1978_M079",
"HK_1978_M078",
"HK_1978_M077",
"HK_1978_M076",
"HK_1978_M075",
"HK_1978_M074",
"HK_1978_M073",
"HK_1978_M072",
"HK_1978_M071",
"HK_1978_M070",
"HK_1978_M067",
"HK_1978_M066",
"HK_1978_M065",
"HK_1978_M064",
"HK_1978_M059",
"HK_1978_M058",
"HK_1978_M057",
"HK_1978_M056",
"HK_1978_M055",
"HK_1978_M052",
"HK_1978_M051",
"HK_1978_M050",
"HK_1978_M049",
"HK_1978_M048",
"HK_1978_M047",
"HK_1978_M046",
"HK_1978_M045",
"HK_1978_M044",
"HK_1978_M043",
"HK_1978_M042",
"HK_1978_M041",
"HK_1978_M040",
"HK_1978_M039",
"HK_1978_M038",
"HK_1978_M037",
"HK_1978_M036",
"HK_1978_M035",
"HK_1978_M034",
"HK_1978_M033",
"HK_1978_M032",
"HK_1978_M031",
"HK_1978_M030",
"HK_1978_M029",
"HK_1978_M028",
"HK_1978_M020",
"HK_1978_M019",
"HK_1978_M018",
"HK_1978_M017",
"HK_1978_M016",
"HK_1978_M013",
"HK_1978_M012",
"HK_1978_M011",
"HK_1978_M010",
"HK_1978_M009",
"HK_1978_M008",
"HK_1978_M007",
"HK_1978_M006",
"HK_1978_M005",
"HK_1978_M002",
"HK_1978_M001",
"HK_1977_L182",
"HK_1977_L181",
"HK_1977_L180",
"HK_1977_L179",
"HK_1977_L178",
"HK_1977_L177",
"HK_1977_L176",
"HK_1977_L175",
"HK_1977_L173",
"HK_1977_L171",
"HK_1977_L170",
"HK_1977_L169",
"HK_1977_L168",
"HK_1977_L167",
"HK_1977_L164",
"HK_1977_L163",
"HK_1977_L162",
"HK_1977_L161",
"HK_1977_L160",
"HK_1977_L159",
"HK_1977_L157",
"HK_1977_L156",
"HK_1977_L152",
"HK_1977_L151",
"HK_1977_L150",
"HK_1977_L149",
"HK_1977_L148",
"HK_1977_L147",
"HK_1977_L146",
"HK_1977_L142",
"HK_1977_L141",
"HK_1977_L135",
"HK_1977_L134",
"HK_1977_L133",
"HK_1977_L132",
"HK_1977_L131",
"HK_1977_L130",
"HK_1977_L129",
"HK_1977_L127",
"HK_1977_L126",
"HK_1977_L125",
"HK_1977_L124",
"HK_1977_L123",
"HK_1977_L117",
"HK_1977_L115",
"HK_1977_L114",
"HK_1977_L112",
"HK_1977_L111",
"HK_1977_L110",
"HK_1977_L109",
"HK_1977_L108",
"HK_1977_L106",
"HK_1977_L104",
"HK_1977_L102",
"HK_1977_L101",
"HK_1977_L100",
"HK_1977_L099",
"HK_1977_L098",
"HK_1977_L095",
"HK_1977_L092",
"HK_1977_L091",
"HK_1977_L090",
"HK_1977_L089",
"HK_1977_L088",
"HK_1977_L087",
"HK_1977_L086",
"HK_1977_L085",
"HK_1977_L084",
"HK_1977_L081",
"HK_1977_L080",
"HK_1977_L071",
"HK_1977_L070",
"HK_1977_L067",
"HK_1977_L066",
"HK_1977_L065",
"HK_1977_L064",
"HK_1977_L063",
"HK_1977_L062",
"HK_1977_L058",
"HK_1977_L057",
"HK_1977_L056",
"HK_1977_L055",
"HK_1977_L053",
"HK_1977_L052",
"HK_1977_L051",
"HK_1977_L050",
"HK_1977_L047",
"HK_1977_L046",
"HK_1977_L045",
"HK_1977_L043",
"HK_1977_L042",
"HK_1977_L041",
"HK_1977_L040",
"HK_1977_L039",
"HK_1977_L038",
"HK_1977_L037",
"HK_1977_L036",
"HK_1977_L035",
"HK_1977_L034",
"HK_1977_L033",
"HK_1977_L032",
"HK_1977_L030",
"HK_1977_L028",
"HK_1977_L027",
"HK_1977_L026",
"HK_1977_L025",
"HK_1977_L024",
"HK_1977_L023",
"HK_1977_L022",
"HK_1977_L021",
"HK_1977_L020",
"HK_1977_L019",
"HK_1977_L018",
"HK_1977_L017",
"HK_1977_L016",
"HK_1977_L015",
"HK_1977_L014",
"HK_1977_L012",
"HK_1977_L010",
"HK_1977_L009",
"HK_1977_L008",
"HK_1977_L007",
"HK_1977_L006",
"HK_1977_L003",
"HK_1977_L002",
"HK_1977_L001",
"HK_1976_K141",
"HK_1976_K140",
"HK_1976_K138",
"HK_1976_K137",
"HK_1976_K136",
"HK_1976_K134",
"HK_1976_K133",
"HK_1976_K132",
"HK_1976_K131",
"HK_1976_K130",
"HK_1976_K129",
"HK_1976_K127",
"HK_1976_K124",
"HK_1976_K123",
"HK_1976_K122",
"HK_1976_K121",
"HK_1976_K120",
"HK_1976_K119",
"HK_1976_K118",
"HK_1976_K117",
"HK_1976_K113",
"HK_1976_K112",
"HK_1976_K110",
"HK_1976_K109",
"HK_1976_K106",
"HK_1976_K103",
"HK_1976_K102",
"HK_1976_K101",
"HK_1976_K098",
"HK_1976_K095",
"HK_1976_K094",
"HK_1976_K093",
"HK_1976_K089",
"HK_1976_K088",
"HK_1976_K087",
"HK_1976_K083",
"HK_1976_K082",
"HK_1976_K081",
"HK_1976_K080",
"HK_1976_K079",
"HK_1976_K078",
"HK_1976_K076",
"HK_1976_K075",
"HK_1976_K074",
"HK_1976_K072",
"HK_1976_K071",
"HK_1976_K062",
"HK_1976_K061",
"HK_1976_K060",
"HK_1976_K059",
"HK_1976_K058",
"HK_1976_K056",
"HK_1976_K054",
"HK_1976_K053",
"HK_1976_K052",
"HK_1976_K050",
"HK_1976_K048",
"HK_1976_K047",
"HK_1976_K046",
"HK_1976_K043",
"HK_1976_K041",
"HK_1976_K040",
"HK_1976_K038",
"HK_1976_K036",
"HK_1976_K035",
"HK_1976_K032",
"HK_1976_K031",
"HK_1976_K029",
"HK_1976_K028",
"HK_1976_K027",
"HK_1976_K026",
"HK_1976_K022",
"HK_1976_K020",
"HK_1976_K019",
"HK_1976_K018",
"HK_1976_K017",
"HK_1976_K016",
"HK_1976_K015",
"HK_1976_K006",
"HK_1976_K004",
"HK_1976_K003",
"HK_1976_K001"

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
#table_row_xpath =""
#table_row_xpath = "//div/table[4]/tbody/tr"




Horse_Name_xpath ="/html/body/div/div/table[1]/tbody/tr/td[1]/table/tbody/tr[1]/td"
Horse_Info1_xpath = "/html/body/div/div[1]/table[1]/tbody/tr/td[2]/table"
Horse_Info2_xpath = "/html/body/div/div[1]/table[1]/tbody/tr/td[3]/table"


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
Horse_Info1 = ""
Horse_Info2 = ""

# Begin grabbing data
for horseid in brandno:
  print("Scraping: " + horseid)
  race_entry = []
  count += 1
  if os.path.isfile('Horse_Info_' + str(horseid) + '.txt'):
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

    #tempTableEl = wait.until(EC.presence_of_all_elements_located((By.XPATH, table_row_xpath)))
    #table_rows = tempTableEl

    if (check_exists_by_xpath(Horse_Name_xpath)):
      tempEl = wait.until(EC.presence_of_element_located((By.XPATH, Horse_Name_xpath)))
      horse_name = (tempEl.text)
    if (check_exists_by_xpath(Horse_Info1_xpath)):
      tempEl = wait.until(EC.presence_of_element_located((By.XPATH, Horse_Info1_xpath)))
      Horse_Info1 = (tempEl.text)
    if (check_exists_by_xpath(Horse_Info2_xpath)):
      tempEl = wait.until(EC.presence_of_element_located((By.XPATH, Horse_Info2_xpath)))
      Horse_Info2 = (tempEl.text)
    

  rowEntry = []

  rowEntry.append(horseid)
  rowEntry.append(horse_name)

  rowEntry.append(Horse_Info1)
  rowEntry.append(Horse_Info2)
  race_entry.append(rowEntry)

          
  # Save file as csv
  df = pd.DataFrame(race_entry)
  print(df.head())
  csv_data = df.to_csv("./Horse_Info_" + str(horseid) + ".txt", index=False)
  print("Saved " + str(horseid))

driver.quit()
