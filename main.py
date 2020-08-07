from Scrapers.scraper_race_dates import get_dates
import config

def main():
  # Initialize config object (dates)
  conf = config.Config()
  print(conf.get_historic_dates())

  # Current dates

if __name__ == "__main__":
  main()