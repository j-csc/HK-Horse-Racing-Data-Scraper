from scrapers.scraper_race_dates import get_dates
from scrapers.scraper_racecard import scrape_racecard
from scrapers.scraper_racecard_info import scrape_racecard_info
from scrapers.scraper_horse_info_all import scrape_horse_info
from scrapers.scraper_horse_veterinary_records import scrape_horse_veterinary_records
from scrapers.scraper_penetrometer import scrape_penetrometer
from scrapers.scraper_horse_roarers import scrape_horse_roarer
import config

def main():
  # Initialize config object (dates)
  conf = config.Config()
  hist_dates = (conf.get_historic_dates())

  # Current dates
  # get_dates()

  # Get racecard (not done)
  # scrape_racecard(hist_dates)

  # Get racecard info (not done)
  # scrape_racecard_info(hist_dates)

  # Get all horse info
  # scrape_horse_info()

  # Get all horse veterinary records
  # scrape_horse_veterinary_records()

  # Get all penetrometer readings
  # scrape_penetrometer(hist_dates)

  # Get all horse roarers
  scrape_horse_roarer()
  


if __name__ == "__main__":
  main()