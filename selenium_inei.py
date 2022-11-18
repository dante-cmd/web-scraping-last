##########################################################
# -----------------LEARN SELENIUM ----------------------
##########################################################

# Selenium 3.0 offers three important tools, Selenium WebDriver, Selenium Server, and
# Selenium IDE.
import selenium

print(selenium.__version__)
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from pathlib import Path
from urllib.parse import urljoin

driver_path = r'C:\dchrome\chromedriver.exe'
ser = Service(driver_path)
opt = webdriver.ChromeOptions()

browser = webdriver.Chrome(service=ser, options=opt)
browser.get('http://iinei.inei.gob.pe/microdatos/')

time.sleep(1)

# CONSULTA POR ENCUESTAS
try:
    element = WebDriverWait(browser, 5)\
        .until(EC.element_to_be_clickable((By.XPATH, '//html/body//ul//li//a[contains(@href,"ConsultaPorEncuesta")]')))
    #print(element.text)
    #print(element)
    element.click()
except :
    print('Consulta por encuesta')


# SPAN (TRIANGLE SHAPE)
try:
    element = WebDriverWait(browser, 5)\
        .until(EC.element_to_be_clickable((By.XPATH, '//span[contains(@class, "arrow")]')))
    element.click()
except:
    print('SPAN (TRIANGLE SHAPE)')

# SELECT ENAHO METODOLOGÍAS ACTUALIZA

try:
    element = WebDriverWait(browser, 5)\
        .until(EC.element_to_be_clickable((By.XPATH, '/html/body/span/span/span[2]/ul/li[3]')))
    element.click()
except:
    print('SELECT ENAHO METODOLOGÍAS ACTUALIZA')

# SPAN (TRIANGLE SHAPE) TO SELECT IF ENAHO OR ENAHO PANEL
try:
    element = WebDriverWait(browser, 5)\
        .until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div/div[4]/div/form[1]/div[5]/div[2]/select")))
    element.click()

except:
    print('SPAN (TRIANGLE SHAPE) TO SELECT IF ENAHO OR ENAHO PANEL')

# SELECT CONDICIONES DE VIDA Y POBREZA - ENAHO
try:

    element = WebDriverWait(browser, 5)\
        .until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div/div[4]/div/form[1]/div[5]/div[2]/select/option[2]')))
    element.click()
except:
    print(('SELECT CONDICIONES DE VIDA Y POBREZA - ENAHO'))

#'/html/body/div[2]/div/div/div[4]/div/form[1]/div[5]/div[3]/div[2]/div/select/option[18]'
#years = range(8, 10)

# data_element = {}
years = range(2010, 2021)

data = []
for year in years:

    data_element = {}
    # AÑO
    try:
        element = WebDriverWait(browser, 5)\
            .until(EC.element_to_be_clickable((By.XPATH, '//select[contains(@name, "cmbAnno")]')))
        element.click()
        time.sleep(1)
    except:
        print('AÑO1', year)

    try:
        element = WebDriverWait(browser, 5)\
            .until(EC.element_to_be_clickable((By.XPATH, f'//select[contains(@name, "cmbAnno")]//option[contains(@value,"{year}")]')))
        data_element['year'] = element.text
        element.click()
        time.sleep(1)
    except:
        print('select Año', year)

    # PERIODO
    try:
        element = WebDriverWait(browser, 5)\
            .until(EC.element_to_be_clickable((By.XPATH, '//select[contains(@name, "cmbTrimestre")]')))
        element.click()
        time.sleep(1)
    except:
        print('PERIODO', year)
    try:

        element = WebDriverWait(browser, 5)\
            .until(EC.element_to_be_clickable((By.XPATH, '//select[contains(@name,"cmbTrimestre")]//option[contains(@value,"55")]')))
        data_element['periodo'] = element.text
        element.click()
        time.sleep(1)
    except:
        print('selct PERIODO1', year)

    # DOWNLOAD

    element = WebDriverWait(browser, 5)\
        .until(EC.element_to_be_clickable((By.XPATH, '//td//a[contains(@href, "03.zip") and contains(@href, "SPSS")]')))
    path_name_file = element.get_attribute('href')
    data_element['path_zip_inei'] = urljoin('http://iinei.inei.gob.pe/microdatos/',path_name_file )

    name_file = path_name_file.split('/')[-1]

    path_inint = Path(r'C:\Users\LENOVO\Downloads')

    element.click()

    while not (path_inint / name_file).exists():
        print('Espere 10 segundos')
        time.sleep(10)

    print(f'Downloaded file {name_file}')
    data.append(data_element)
    del element

# browser.quit()



