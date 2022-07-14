from selenium import webdriver
import pytest
pytest.driver = webdriver.Chrome('c:/driver/chromedriver.exe')



@pytest.fixture(autouse=True)
def testing():
   pytest.driver = webdriver.Chrome('c:/driver/chromedriver.exe')

   pytest.driver.implicitly_wait(5)
   # Переходим на страницу авторизации
   pytest.driver.get('http://petfriends.skillfactory.ru/login')
   # Вводим email
   pytest.driver.find_element_by_id('email').send_keys('erigov@mail.ru')

   # Вводим пароль
   pytest.driver.find_element_by_id('pass').send_keys('qwe123')

   btn_submit = pytest.driver.find_element_by_xpath("//button[@type='submit']")
   btn_submit.click()

   pytest.driver.get('https://petfriends.skillfactory.ru/my_pets')

   yield

   pytest.driver.quit()