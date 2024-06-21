import pytest
import time

from helper.constant import CandidateFields

from Class.Scraping.Indeed.IndeedScraper import IndeedScraper

LOGIN = "https://secure.indeed.com/auth?continue=https%3A%2F%2Femployers.indeed.com%2Fcandidates%2Fview%3Fid%3Da7818f403e05%26l%3DveUW%26listQuery%3Dc3RhdHVzTmFtZSUzREFjdGl2ZSUyNnNlbGVjdGVkSm9icyUzRGFYSnBPaTh2WVhCcGN5NXBibVJsWldRdVkyOXRMMFZ0Y0d4dmVXVnlTbTlpTDJVeU1ERTROREV5TFdGak16QXROREF4WlMwNFpUUmtMV0pqWTJGaU1XTTVObVJqTmclMjUzRCUyNTNEJTI2aWQlM0QxNjRkMGZkMjZlNjM%253D%26lName%3DnextPreviousCandidateList%26pos%3D11%26from%3Dgnav-util-one-host&hl=es&co=PE&userType=employer"
JOB_PAGE = "https://employers.indeed.com/candidates?statusName=Active&id=164d0fd26e63&selectedJobs=aXJpOi8vYXBpcy5pbmRlZWQuY29tL0VtcGxveWVySm9iL2UyMDE4NDEyLWFjMzAtNDAxZS04ZTRkLWJjY2FiMWM5NmRjNg%3D%3D"
USER_EMAIL = "pe.dominguezjosejuan@gmail.com"
HOME = "https://employers.indeed.com/candidates/view?id=a7818f403e05&l"

@pytest.fixture(scope="module")
def login():
    ind = IndeedScraper()
    ind.start_browser()
    ind.login(
        login_url=LOGIN,
        user_email=USER_EMAIL,
    )
    yield ind

def test_home_page(login):
    l = login
    time.sleep(5)

    assert HOME in l.scraper.driver.current_url

@pytest.fixture(scope="module")
def job_page(login):
    time.sleep(3)
    login.job_post(JOB_PAGE)
    yield login

def test_job_post_url(job_page):
    
    assert job_page.scraper.driver.current_url == JOB_PAGE

def test_first_candidate(job_page):
    j = job_page
    j.press_on_first_candidate()
    time.sleep(3)

    assert 'view' in j.scraper.driver.current_url
    
def test_load_all_candidates(job_page):
    j = job_page
    j.press_on_first_candidate()
    time.sleep(3)
    j.load_all_candidates()
    j.get_candidates()
    candidate_generator = j.loop_candidates()        
    candidate_data_generator = j.extract_candidate_data(candidate_generator)
    for candidate in candidate_data_generator:
        
        j.candidates.append(candidate)
        break
    
    can = j.candidates[0]
    assert type(can[CandidateFields.NAME.value]) == str
    assert type(can[CandidateFields.PHONE.value]) == str
    assert type(can[CandidateFields.EMAIL.value]) == str
    assert type(can[CandidateFields.DNI.value]) == str
    assert type(can[CandidateFields.ADDRESS.value]) == str
    assert type(can[CandidateFields.AGE.value]) == str
    assert type(can[CandidateFields.WORK_EXPERIENCE.value]) == str
    assert type(can[CandidateFields.STUDY.value]) == str
    assert type(can[CandidateFields.SKILL.value]) == str
    assert type(can[CandidateFields.PLATAFORM.value]) == str
    
    assert len(can[CandidateFields.NAME.value]) > 0
    assert len(can[CandidateFields.PHONE.value]) > 0
    assert len(can[CandidateFields.EMAIL.value]) > 0
    assert len(can[CandidateFields.DNI.value]) > 0
    assert len(can[CandidateFields.ADDRESS.value]) > 0
    assert len(can[CandidateFields.AGE.value]) > 0
    assert len(can[CandidateFields.WORK_EXPERIENCE.value]) > 0
    assert len(can[CandidateFields.STUDY.value]) > 0
    assert len(can[CandidateFields.SKILL.value]) > 0
    assert len(can[CandidateFields.PLATAFORM.value]) > 0

    
def test_load_all_candidates(job_page):
    j = job_page
    j.press_on_first_candidate()
    time.sleep(3)
    j.load_all_candidates()
    j.get_candidates()

    assert len(j.candidates_webelement) > 35

# @pytest.fixture(scope="module")
# def candidates_links(job_page):
#     com = job_page
#     com.get_candidates_links()
#     yield com

# def test_candidates(candidates_links):
#     com = candidates_links

#     assert len(com.candidates_links) == 75

# def test_candidate_data(candidates_links):
#     com = candidates_links
#     candidate_generator = com.loop_candidates()
#     candidate_data_generator = com.extract_candidate_data(candidate_generator)

#     for candidate_data in candidate_data_generator:
#         candidate = candidate_data
#         break

#     name = CandidateFields.NAME.value
#     phone = CandidateFields.PHONE.value
#     email = CandidateFields.EMAIL.value
#     dni = CandidateFields.DNI.value
#     address = CandidateFields.ADDRESS.value
#     age = CandidateFields.AGE.value
#     experience = CandidateFields.WORK_EXPERIENCE.value
#     study = CandidateFields.STUDY.value
#     skills = CandidateFields.SKILL.value

#     assert type(candidate[name]) == str
#     assert candidate[name].lower() != "Sin Nombre".lower()
#     assert len(candidate[name]) > 1

#     assert type(candidate[phone]) == str
#     assert candidate[phone].lower() != "Sin Telefono".lower()
#     assert len(candidate[phone]) > 1

#     assert type(candidate[email]) == str
#     assert candidate[email].lower() != "Sin correo".lower()
#     assert len(candidate[email]) > 1

#     assert type(candidate[address]) == str
#     assert candidate[address].lower() != "Sin direccion".lower()
#     assert len(candidate[address]) > 1

#     assert type(candidate[age]) == str
#     assert candidate[age].lower() != "Sin Edad".lower()
#     assert len(candidate[age]) > 1

#     assert type(candidate[dni]) == str
#     assert candidate[dni].lower() != "Sin dni".lower()
#     assert len(candidate[dni]) > 1

#     assert type(candidate[experience]) == list
#     assert len(candidate[experience]) >= 1
#     assert candidate[experience][0].lower() != "Sin experiencia".lower()

#     assert type(candidate[study]) == list
#     assert len(candidate[study]) >= 1
#     assert candidate[study][0].lower() != "Sin estudio".lower()
    
#     assert type(candidate[skills]) == list
#     assert len(candidate[skills]) >= 1
#     assert candidate[skills][0].lower() != "Sin habilidades".lower()

# @pytest.fixture(scope="module")
# def scraping(job_page):
#     com = job_page
#     com.start_scraping()

#     yield com

# def test_start_scraping(scraping):
#     com = scraping
#     assert len(com.candidates) == 75

# def test_saved_data(scraping):
#     com = scraping
#     com.save_css_file(job_position_name="testing_file")
