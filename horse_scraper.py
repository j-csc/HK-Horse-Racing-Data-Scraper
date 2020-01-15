#import libraries 
import requests
import string
import json
import itertools 
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from bs4 import BeautifulSoup

#starting the webdriver
driver = webdriver.Firefox()
alphabets = string.ascii_uppercase
wait = WebDriverWait(driver, 10)

def check_all_xpath_exists(xpaths):
  for xpath in xpaths:
    try:
      driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
      return False
  return True

def check_exists_by_xpath(xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True


names = list() 
country_of_origin_age = list()
country_of_origin_age_xpath = "///div[1]/table[1]/tbody/tr/td[2]/table/tbody/tr[1]/td[3]"
colour_sex = list()
colour_sex_xpath = "//div[1]/table[1]/tbody/tr/td[2]/table/tbody/tr[2]/td[3]"
import_type = list()
import_type_xpath = "//div[1]/table[1]/tbody/tr/td[2]/table/tbody/tr[3]/td[3]"
season_stakes = list()
season_stakes_xpath = "//div[1]/table[1]/tbody/tr/td[2]/table/tbody/tr[4]/td[3]"
total_stakes = list()
total_stakes_xpath = "//div[1]/table[1]/tbody/tr/td[2]/table/tbody/tr[5]/td[3]"
no_of_123_starts = list()
no_of_123_starts_xpath = "//div[1]/table[1]/tbody/tr/td[2]/table/tbody/tr[6]/td[3]" 
no_of_starts_in_past_races = list()
no_of_starts_in_past_races_xpath = "//div[1]/table[1]/tbody/tr/td[2]/table/tbody/tr[7]/td[3]"
trainer = list()
trainer_xpath = "//div[1]/table[1]/tbody/tr/td[3]/table/tbody/tr[1]/td[3]/a"
owner = list()
owner_xpath = "//div[1]/table[1]/tbody/tr/td[3]/table/tbody/tr[2]/td[3]/a"
current_rating = list()
current_rating_xpath = "//div[1]/table[1]/tbody/tr/td[3]/table/tbody/tr[3]/td[3]"
start_of_season_rating = list()
start_of_season_rating_xpath = "//div[1]/table[1]/tbody/tr/td[3]/table/tbody/tr[4]/td[3]"
sire = list()
sire_xpath = "//div[1]/table[1]/tbody/tr/td[3]/table/tbody/tr[5]/td[3]"
dam = list()
dam_xpath = "//div[1]/table[1]/tbody/tr/td[3]/table/tbody/tr[6]/td[3]"
dam_sire = list()
dam_sire_xpath = "//div[1]/table[1]/tbody/tr/td[3]/table/tbody/tr[7]/td[3]"

all_xpaths = [country_of_origin_age_xpath, colour_sex_xpath, import_type_xpath, season_stakes_xpath, total_stakes_xpath, no_of_123_starts_xpath,
  no_of_starts_in_past_races_xpath, trainer_xpath, owner_xpath,
  current_rating_xpath,start_of_season_rating_xpath,sire_xpath,dam_xpath,dam_sire_xpath]

alphabet_link = "http://racing.hkjc.com/racing/information/English/Horse/SelectHorsebyChar.aspx?ordertype="
horse_link_xpath = "//p/table/tbody/tr[2]/td/table/tbody"

# For individual horses
driver.implicitly_wait(2)

for i in alphabets:
  print("Scraping " + i)
  driver.get(alphabet_link + i)
  driver.implicitly_wait(2)
  wait.until(EC.presence_of_element_located((By.XPATH, horse_link_xpath)))
  horse_table = driver.find_elements_by_xpath(horse_link_xpath)
  print(horse_table)
  for h in horse_table:
    row_links = h.find_elements_by_tag_name("a")
    indiv_horse_links = list()
    for item in row_links:
      indiv_horse_links.append(item.get_attribute("href"))
      names.append(item.text)
    for indiv_horse_link in indiv_horse_links:
      driver.get(indiv_horse_link)
      driver.implicitly_wait(2)
      if check_all_xpath_exists(all_xpaths):
        country_of_origin_age.append(driver.find_element_by_xpath(country_of_origin_age_xpath))
        colour_sex.append(driver.find_element_by_xpath(colour_sex_xpath))
        import_type.append(driver.find_element_by_xpath(import_type_xpath))
        season_stakes.append(driver.find_element_by_xpath(season_stakes_xpath))
        total_stakes.append(driver.find_element_by_xpath(total_stakes_xpath))
        no_of_123_starts.append(driver.find_element_by_xpath(no_of_123_starts_xpath))
        no_of_starts_in_past_races.append(driver.find_element_by_xpath(no_of_starts_in_past_races_xpath))
        trainer.append(driver.find_element_by_xpath(trainer_xpath).text)
        owner.append(driver.find_element_by_xpath(owner_xpath).text)
        current_rating.append(driver.find_element_by_xpath(current_rating_xpath))
        start_of_season_rating.append(driver.find_element_by_xpath(start_of_season_rating_xpath))
        sire.append(driver.find_element_by_xpath(sire_xpath).text)
        dam.append(driver.find_element_by_xpath(dam_xpath))
        dam_sire.append(driver.find_element_by_xpath(dam_sire_xpath))

data = [{'Name': a, 'Country of Origin & Age': b, 'Colour & Sex': c, 'Import Type': d, 'Season Stakes': e, 'Total Stakes': f, 'Number Of 123 Starts': g, 'Number of Starts In Past Races': h, 'Trainer': i, 'Owner': j, 'Current Rating': k, 'Start Of Season Rating': l, 'Sire': m, 'Dam': n, 'Dam Sire': o } for a, b, c, d, e, f, g, h, i, j, k, l, m, n, o in zip(names, country_of_origin_age, colour_sex,import_type, season_stakes, total_stakes, no_of_starts_in_past_races, no_of_starts_in_past_races, trainer, owner, current_rating, start_of_season_rating, sire, dam, dam_sire)]

with open('horses.json', 'w') as outfile:
  json.dump(data, outfile)