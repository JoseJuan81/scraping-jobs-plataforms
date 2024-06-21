import time

from Class.Scraping.Computrabajo.ComputrabajoScraper import ComputrabajoScraper
from Class.Terminal.CommandLine import CommandLine

terminal_input = CommandLine()

if __name__ == "__main__":
    comp = ComputrabajoScraper()
    comp.start_browser()
    comp.login(
        login_url=terminal_input.login_url,
        user_pass=terminal_input.user_pass,
        user_email=terminal_input.user_email
    )

    time.sleep(3)

    comp.job_post(terminal_input.job_url)
    comp.start_scraping()
    comp.save_css_file(job_position_name=terminal_input.process_name)
    comp.end(job_position_name=terminal_input.process_name)