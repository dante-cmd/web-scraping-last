##########################################################
# -----------------LEARN SELENIUM ----------------------
##########################################################

# Selenium 3.0 offers three important tools, Selenium WebDriver, Selenium Server, and
# Selenium IDE.
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from pathlib import Path
from urllib.parse import urljoin


class GetDataINEI:
    def __init__(self):
        driver_path = r'C:\dmozilla\geckodriver.exe'
        ser = Service(driver_path)
        opt = webdriver.FirefoxOptions()
        self.driver = webdriver.Firefox(service=ser, options=opt)
    
    def goToINEI(self):
        self.driver.get('https://iinei.inei.gob.pe/microdatos/')

    def clickOnElement(self, method, param):
        try:
            element = WebDriverWait(self.driver, 5)\
                .until(lambda d:d.find_element(method, param))
            element.click()
            return True

        except Exception as e:
            print(e.args)
            return False
    
    def goToRange(self):
        # => Click on Consulta Por Encuesta
        self.clickOnElement(By.XPATH, '//ul[@id="jsmenu"]//li//a[contains(@href,"ConsultaPorEncuesta")]')
        # => Click On options
        self.clickOnElement(By.XPATH,'//span[contains(@class, "arrow")]')
        # => 
        self.clickOnElement(
            By.XPATH,
            '//ul[@class="select2-results__options"]//li[3]')
        
        self.clickOnElement(
            By.NAME,
            'cmbEncuestaN')
        self.clickOnElement(
            By.XPATH, "//select[@name='cmbEncuestaN']//option[@value='Condiciones de Vida y Pobreza - ENAHO']"
        )

    def isDownloaded(self):
        
        path_download = Path('C:/Users/LENOVO/Downloads')
        while list(path_download.glob('*Modulo03*.zip.part')):
            print('sleep 5 seconds')
            time.sleep(5)
        
        return True
        # '279-Modulo03.qg1gB-tn.zip.part'

    def dowloadByYear(self, year):
        option_year = self.clickOnElement(
                By.XPATH, f"//select[@name='cmbAnno']//option[@value='{year}']"
            )
        option_period = self.clickOnElement(
                By.XPATH, "//select[@name='cmbTrimestre']//option[@value='55']"
            )
        if option_period and option_year:
            time.sleep(10)

            self.clickOnElement(
                    By.XPATH, '//td//a[contains(@href, "03.zip") and contains(@href, "SPSS")]'
                )

    def downloadHistorical(self):
        years = range(2010, 2022)
        for year in years:
            self.dowloadByYear(year)
            if self.isDownloaded():
                continue
    
    def quit(self):
        self.driver.quit()
        
if __name__ == '__main__':
    inei = GetDataINEI()
    inei.goToINEI()
    inei.goToRange()
    inei.downloadHistorical()
    inei.quit()
    # inei.dowloadByYear(2023)