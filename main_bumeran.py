from Class.Scraping.Bumeran.BumeranScraper import BumeranScraper

JOB_PAGE = "https://www.bumeran.com.pe/empresas/postulaciones?idAviso=1116307021"

if __name__ == "__main__":
    bum = BumeranScraper()
    bum.start_browser()
    bum.login()
    bum.job_post()
    bum.start_scraping()
    bum.API.send(url="")
    # bum.end()