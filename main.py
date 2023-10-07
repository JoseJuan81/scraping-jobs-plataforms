"""Módulo de inicio para hacer scraping en computrabajo"""

from Class.Scraper import Scraper
from helper.ghl import GHL_APP


if __name__ == "__main__":
    scraper = Scraper()
    scraper.init()
    scraper.use_external_api(send=False)
    scraper.list_of_candidates()
    scraper.details_of_candidate()
    scraper.end()
