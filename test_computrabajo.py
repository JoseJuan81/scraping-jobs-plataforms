import pytest
import time

from helper.constant import CandidateFields

from Class.Scraping.Computrabajo.ComputrabajoScraper import ComputrabajoScraper

LOGIN = "https://empresa.pe.computrabajo.com/Company"
JOB_PAGE = "https://empresa.pe.computrabajo.com/Company/Offers/Match?oi=F9669F7CB1D08CA961373E686DCF3405&cf=469814F59E4D6F04"
USER_EMAIL = "info@japisale.com"
USER_PASS = "MilongoIV8"


@pytest.fixture(scope="module")
def login():
    com = ComputrabajoScraper()
    com.start_browser()
    com.login(
        login_url=LOGIN,
        user_email=USER_EMAIL,
        user_pass=USER_PASS
    )
    yield com

def test_home_page(login):
    l = login
    time.sleep(5)

    assert l.scraper.driver.current_url == LOGIN

@pytest.fixture(scope="module")
def job_page(login):
    time.sleep(3)
    login.job_post(JOB_PAGE)
    yield login

def test_job_post_url(job_page):
    
    assert job_page.scraper.driver.current_url == JOB_PAGE

@pytest.fixture(scope="module")
def candidates_links(job_page):
    com = job_page
    com.get_candidates_links()
    yield com

def test_candidates(candidates_links):
    com = candidates_links

    assert len(com.candidates_links) == 75

def test_candidate_data(candidates_links):
    com = candidates_links
    candidate_generator = com.loop_candidates()
    candidate_data_generator = com.extract_candidate_data(candidate_generator)

    for i, candidate_data in enumerate(candidate_data_generator):
        if i == 0:
            candidate = candidate_data
            break

    name = CandidateFields.NAME.value
    image = CandidateFields.IMAGE.value
    phone = CandidateFields.PHONE.value
    email = CandidateFields.EMAIL.value
    dni = CandidateFields.DNI.value
    address = CandidateFields.ADDRESS.value
    age = CandidateFields.AGE.value
    # profile_page = CandidateFields.PROFILE_PAGE.value
    # application_time = CandidateFields.APPLICATION_TIME.value
    experience = CandidateFields.WORK_EXPERIENCE.value
    study = CandidateFields.STUDY.value
    skills = CandidateFields.SKILL.value
    # match = CandidateFields.MATCH.value
    expectation = CandidateFields.EXPECTATION.value
    summary = CandidateFields.PERSONAL_SUMMARY.value

    assert type(candidate[name]) == str
    assert candidate[name].lower() != "Sin Nombre".lower()
    assert len(candidate[name]) > 1

    assert type(candidate[image]) == str
    # assert candidate[image].lower() != "Sin Imagen".lower()
    assert len(candidate[image]) > 1

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
    assert type(candidate[skills]) == list

    assert type(candidate[summary]) == str
    assert candidate[summary].lower() != "Sin resumen".lower()
    assert len(candidate[summary]) >= 1

    assert type(candidate[expectation]) == str
    assert candidate[expectation].lower() != "Sin Espectativa salarial".lower()
    assert len(candidate[expectation]) > 1


@pytest.fixture(scope="module")
def scraping(job_page):
    com = job_page
    com.start_scraping()

    yield com

def test_start_scraping(scraping):
    com = scraping
    assert len(com.candidates) == 75

def test_saved_data(scraping):
    com = scraping
    com.save_css_file(job_position_name="testing_file")
