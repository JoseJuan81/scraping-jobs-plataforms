import time

from Class.Scraping.Bumeran.BumeranScraper import BumeranScraper
from Class.Terminal.CommandLine import CommandLine

terminal_input = CommandLine()

if __name__ == "__main__":
    bum = BumeranScraper()
    bum.start_browser()
    bum.login(
        login_url=terminal_input.login_url,
        user_pass=terminal_input.user_pass,
        user_email=terminal_input.user_email
    )
    
    time.sleep(3)

    bum.job_post(terminal_input.job_url)
    bum.start_scraping()
    bum.API.send(url="")
    # bum.end()