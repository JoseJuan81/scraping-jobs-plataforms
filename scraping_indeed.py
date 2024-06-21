import time

from Class.Scraping.Indeed.IndeedScraper import IndeedScraper
from Class.Terminal.CommandLine import CommandLine

terminal_input = CommandLine()

if __name__ == "__main__":
    indeed = IndeedScraper()
    indeed.start_browser()
    indeed.login(
        login_url=terminal_input.login_url,
        user_email=terminal_input.user_email
    )

    time.sleep(3)

    indeed.job_post(terminal_input.job_url)
    indeed.start_scraping()
    indeed.save_css_file(job_position_name=terminal_input.process_name)
    indeed.end(job_position_name=terminal_input.process_name)