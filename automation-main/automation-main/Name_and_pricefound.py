# This file has all the functions within a class to perform task
# Here my object or instance is session
import glob
import os.path
import time
from PIL import Image
import pytesseract
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common import by
from constants import loginpage_address
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options


class execution_of_orders(webdriver.Chrome):  # Objects or instance of Execution of Orders can use methods of both
    # superclass(webdriver.chrome) and child class(execution_of_orders)
    def __init__(self, driverpath='chromedriver.exe'):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        self.driverpath = driverpath  # Instance variable driverpath is declared which stores location of driverpath which is very important for automation
        super(execution_of_orders, self).__init__()

    def login(self, username, password):
        self.get(loginpage_address)  # Now the login page gets open
        login_userid = self.find_element_by_id('email')
        login_password = self.find_element_by_id('password')
        login_userid.send_keys(username)
        login_password.send_keys(password)  # Here my login completes
        self.find_element_by_class_name('g-recaptcha').click()
        time.sleep(1)

    def open_screener(self, screener_link):
        self.get(screener_link)
        self.implicitly_wait(5)


    def runscan(self):
        self.find_element_by_class_name('run_scan_button').click()
        # Explicit wait can reached by the use of WebDriverWait
        WebDriverWait(self, 20).until(
            EC.text_to_be_present_in_element(
                (By.CLASS_NAME, 'run_scan_button'),
                "Running.."
            )
        )

    def list_of_stocks(self):
        list_of_symbols = []
        list_of_urls = []
        i = 1
        k =0
        while i < 26:
            try:

                j = str(i)
                s = ''
                stock_rel_xpath = list('//tbody/tr[1]/td[2]/a[1]')
                stock_name_rel_xpath = list('//tbody/tr[1]/td[3]/a[1]')
                stock_rel_xpath[11] = j
                stock_name_rel_xpath[11] = j
                new_rel_xpath = stock_rel_xpath
                new_stock_name_rel_xpath = stock_name_rel_xpath
                element = self.find_element_by_xpath(s.join(new_rel_xpath))
                element_symbol=self.find_element_by_xpath(s.join(new_stock_name_rel_xpath))
                list_of_urls.append(element.get_attribute('href'))
                list_of_symbols.append(element_symbol.text)
                k=i
                i = i + 1
                time.sleep(2)
            except:  # NoSuchElementException
                break

        return list_of_urls,list_of_symbols,k # where k is total elements

    def supertrend_finder(self,list_urls,j):#Both are in order
        url = list_urls
        l = int(j)
        list_supertrend=[]
        i = 0
        while i < l:
            self.get(url[i])
            if i == 0 : #Normal setting which we need to extract the indicators value
                self.find_element_by_id('RSIm').click()
                time.sleep(0.5)
                self.find_element_by_xpath('//a[normalize-space()="Upper Overlays"]').click()
                time.sleep(0.5)
                self.find_element_by_id('supertrendm').click()
                self.find_element_by_xpath('//input[@name="supertrendl"]').send_keys(Keys.CONTROL, 'a')
                self.find_element_by_xpath('//input[@name="supertrendl"]').send_keys(Keys.BACKSPACE)
                self.find_element_by_xpath('//input[@name="supertrendl"]').send_keys('9,1')
                self.find_element_by_xpath('//a[normalize-space()="Moving Avgs"]').click()
                time.sleep(0.5)
                self.find_element_by_id('a1m').click()
                self.find_element_by_id('a2m').click()
                self.find_element_by_id('ti').send_keys('11')
                time.sleep(0.5)
                self.find_element_by_id('d').click()
                self.find_element_by_id('d').send_keys('111')
                self.find_element_by_id('innerb').click()
                self.switch_to.frame(self.find_element_by_id('ChartImage'))
                download_button = self.find_element_by_id('saverbutton')
                download_button.click()
                self.switch_to.default_content()

                time.sleep(2)

                folder_path = r'C:/Users/Sanyam/Downloads'
                file_type = '/*png'
                files = glob.glob(folder_path + file_type)
                max_file = max(files, key=os.path.getctime)

                img = Image.open(max_file)
                left = 168.9
                top = 50
                right = 225
                bottom = 80
                img1 = img.crop((left, top, right, bottom))
                img1 = img1.resize((150, 75))
                img1.show()  # till here code runs fine and have no problem
                text = pytesseract.image_to_string(img1)
                list_supertrend.append(text)
                os.remove(max_file)

                i = i+1

            else :
                self.switch_to.frame(self.find_element_by_id('ChartImage'))
                download_button = self.find_element_by_id('saverbutton')
                download_button.click()
                self.switch_to.default_content()

                time.sleep(2)


                folder_path = r'C:/Users/Sanyam/Downloads'
                file_type = '/*png'
                files = glob.glob(folder_path + file_type)
                max_file = max(files, key=os.path.getctime)

                img = Image.open(max_file)
                left = 168.9
                top = 50
                right = 225
                bottom = 80
                img1 = img.crop((left, top, right, bottom))
                img1 = img1.resize((150, 75))
                img1.show()  # till here code runs fine and have no problem
                text = pytesseract.image_to_string(img1)
                list_supertrend.append(text)
                os.remove(max_file)
                i = i+1

        return list_supertrend