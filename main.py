"""Módulo de inicio para hacer scraping en computrabajo"""

from Class.Scraper import Scraper

if __name__ == "__main__":
    scraper = Scraper()
    scraper.init()
    scraper.list_of_candidates()
    scraper.details_of_candidate()
    scraper.end()
