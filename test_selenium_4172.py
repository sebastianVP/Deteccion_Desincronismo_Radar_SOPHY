from selenium.webdriver import Chrome
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

driver_options = Options()
driver_options.add_argument('--headless')
driver_options.add_argument('--no-sandbox')
driver = webdriver.Chrome()
driver.get("http://sophy/accounts/login/?next=/experiment/1/edit/")
driver.maximize_window()
time.sleep(1)
def slow_typing(element, text):
    for character in text:
        element.send_keys(character)
        time.sleep(0.3)


def ci():
    ci = driver.find_element(By.ID, 'id_username')
    slow_typing(ci, 'developer')#71846355, syañez@igp.gob.pe # 43485084 yellyna
    ci = driver.find_element(By.ID, 'id_password')
    slow_typing(ci, 'developer9')#71846355, syañez@igp.gob.pe # 43485084 yellyna
    time.sleep(2)

def sb():
    submit = driver.find_element(By.CSS_SELECTOR,"button[class='btn btn-primary']")
    submit.click()
    time.sleep(3)

ci()
sb()
driver.get("http://sophy/experiment/1/stop/")
time.sleep(15)
driver.get("http://sophy/experiment/1/start/")
time.sleep(3)
input("Escribe [q] y luego la  tecla [Enter] para finalizar: ")


