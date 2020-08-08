from Scrapers.scraper_race_dates import get_dates
from Scrapers.scraper_racecard import scrape_racecard
from Scrapers.scraper_racecard_info import scrape_racecard_info
from Scrapers.scraper_horse_info_all import scrape_horse_info
from Scrapers.scraper_horse_veterinary_records import scrape_horse_veterinary_records
from Scrapers.scraper_penetrometer import scrape_penetrometer
import config

def main():
  # Initialize config object (dates)
  conf = config.Config()
  hist_dates = (conf.get_historic_dates())

  # Current dates
  # get_dates()

  # Get racecard
  # scrape_racecard(hist_dates)

  # Get racecard info
  # scrape_racecard_info(hist_dates)

  # Get all horse info
  # scrape_horse_info()

  # Get all horse veterinary records
  # scrape_horse_veterinary_records()

  # Get all penetrometer readings
  # scrape_penetrometer(hist_dates)
  


if __name__ == "__main__":
  main()