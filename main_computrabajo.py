from Class.Scraping.Computrabajo.ComputrabajoScraper import ComputrabajoScraper

JOB_PAGE = "https://www.bumeran.com.pe/empresas/postulaciones?idAviso=1116307021"

if __name__ == "__main__":
    comp = ComputrabajoScraper()
    comp.start_browser()
    comp.login()
    comp.job_post()
    comp.start_scraping()
    comp.API.send(url="")