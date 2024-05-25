import pytest
import time

import inspect

from Class.SavingData import SavingData
from helper.constant import CandidateFields

from Class.Scraping.Bumeran.BumeranScraper import BumeranScraper

LOGIN = "https://www.bumeran.com.pe/empresas/ingreso"
JOB_PAGE = "https://www.bumeran.com.pe/empresas/postulaciones?idAviso=1116307021"
USER_EMAIL = "vinimerizalde@gmail.com"
USER_PASS = "M1l1tant3d3lam0r"

@pytest.fixture(scope="module")
def login():
    bum = BumeranScraper()
    bum.start_browser()
    bum.login(
        login_url=LOGIN,
        user_email=USER_EMAIL,
        user_pass=USER_PASS
    )
    yield bum

def test_home_page(login):
    l = login
    time.sleep(5)

    assert l.scraper.driver.current_url == "https://www.bumeran.com.pe/empresas/dashboard"

@pytest.fixture(scope="module")
def job_page(login):
    time.sleep(5)
    login.job_post(JOB_PAGE)

    yield login

def test_candidates(job_page):
    bum = job_page
    bum.get_candidates()

    assert len(bum.candidates_webelements) == 25

def test_loop_candidates(job_page):
    bum = job_page
    bum.get_candidates()
    candidate_generator = bum.loop_candidates()

    assert inspect.isgenerator(candidate_generator)

def test_extract_candidate_data(job_page):
    bum = job_page
    bum.get_candidates()
    candidate_generator = bum.loop_candidates()
    generator = bum.extract_candidate_data(candidate_generator)
    candidate = next(generator)

    name = CandidateFields.NAME.value
    phone = CandidateFields.PHONE.value
    email = CandidateFields.EMAIL.value
    dni = CandidateFields.DNI.value
    address = CandidateFields.ADDRESS.value
    age = CandidateFields.AGE.value
    experience = CandidateFields.WORK_EXPERIENCE.value
    study = CandidateFields.STUDY.value
    skills = CandidateFields.SKILL.value

    assert type(candidate[name]) == str
    assert candidate[name].lower() != "Sin Nombre".lower()
    assert len(candidate[name]) > 1

    assert type(candidate[phone]) == str
    assert candidate[phone].lower() != "Sin Telefono".lower()
    assert len(candidate[phone]) > 1

    assert type(candidate[email]) == str
    assert candidate[email].lower() != "Sin correo".lower()
    assert len(candidate[email]) > 1

    assert type(candidate[address]) == str
    assert candidate[address].lower() != "Sin direccion".lower()
    assert len(candidate[address]) > 1

    assert type(candidate[age]) == str
    assert candidate[age].lower() != "Sin Edad".lower()
    assert len(candidate[age]) > 1

    assert type(candidate[dni]) == str
    assert candidate[dni].lower() != "Sin dni".lower()
    assert len(candidate[dni]) > 1

    assert type(candidate[experience]) == list
    assert len(candidate[experience]) >= 1
    assert candidate[experience][0].lower() != "Sin experiencia".lower()

    assert type(candidate[study]) == list
    assert len(candidate[study]) >= 1
    assert candidate[study][0].lower() != "Sin estudio".lower()
    
    assert type(candidate[skills]) == list
    assert len(candidate[skills]) >= 1
    assert candidate[skills][0].lower() != "Sin habilidades".lower()

def test_save_data():
    candidate = dict([
        (CandidateFields.NAME.value, "JJ"),
        (CandidateFields.PHONE.value, "970127070"),
        (CandidateFields.EMAIL.value, "email@mail.com"),
        (CandidateFields.DNI.value, "0391684"),
        (CandidateFields.ADDRESS.value, "Calle Robinson 213"),
        (CandidateFields.AGE.value, "42"),
        (CandidateFields.WORK_EXPERIENCE.value, "de todo un poco"),
        (CandidateFields.STUDY.value, "Ingenieria MEcanica"),
        (CandidateFields.SKILL.value, "por demas..."),
    ])
    candidates = [candidate]
    SavingData().save_candidates(candidates, "bumeran_pytest_test")

    candidates = [candidate, candidate, candidate]
    SavingData().save_candidates(candidates, "bumeran_pytest_test")

def test_pagination(job_page):
    bum = job_page
    bum.next_page()
    time.sleep(5)

    expected = bum.scraper.get_element(bum.css_selectors.ACTIVE_PAGE).text
    assert int(expected) == 2

    bum.next_page()
    time.sleep(5)
    bum.next_page()
    time.sleep(5)

    expected = bum.scraper.get_element(bum.css_selectors.ACTIVE_PAGE).text
    assert int(expected) == 4

    bum.next_page()
    time.sleep(5)
    bum.next_page()
    time.sleep(5)
    bum.next_page()
    time.sleep(5)
    bum.next_page()
    time.sleep(5)
    bum.next_page()
    time.sleep(5)
    bum.next_page()
    time.sleep(5)
    bum.next_page()
    time.sleep(5)
    bum.next_page()
    time.sleep(5)
    bum.next_page()
    time.sleep(5)
    bum.next_page()
    time.sleep(5)

    expected = bum.scraper.get_element(bum.css_selectors.ACTIVE_PAGE).text
    assert int(expected) == 11

    bum.next_page()
    time.sleep(5)

    expected = bum.scraper.get_element(bum.css_selectors.ACTIVE_PAGE).text
    assert int(expected) == 11

def test_start_scraping(job_page):
    bum = job_page
    bum.start_scraping()

    assert len(bum.candidates) == 25
    assert type(bum.candidates[0]) == dict