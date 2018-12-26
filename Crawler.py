
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import Stocks

class Crawler:

    def __init__(self):
        self.webDriver = webdriver.Chrome()
        self.industries = []
        self.wait_df = 20
        self.wait = WebDriverWait(self.webDriver, self.wait_df)
        self.element_list = []
        self.s = Stocks.Stock()

    def wait_by_xpath(self, xpath):
        self.wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
        self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))

    def load_industries(self, xpath):
        self.element_list = []
        self.element_list = self.webDriver.find_elements_by_xpath(xpath)
        for i in self.element_list:
            self.industries.append(i.get_attribute('title'))

    def extract_stocks(self, xpath):
        self.element_list = []
        self.element_list = self.webDriver.find_elements_by_xpath(xpath)
        for e in self.element_list:
            self.s.ticker = e.text
            self.s.name = e.get_attribute('title')

            print("{} - {}".format(self.s.ticker, self.s.name))

    def crawl(self, url):
        self.webDriver.maximize_window()
        self.webDriver.get(url)

        # Get the titles of all industries in yahoo finance
        self.webDriver.find_element_by_xpath("//a[@title='Industries']").click()

        xpath = "//ul[@data-test='secnav-list']//child::a"
        self.wait_by_xpath(xpath)
        self.load_industries(xpath)

        # iterate through pages for each industry
        for i in self.industries:
            try:
                xpath = "//a[@title='Industries']"
                self.wait_by_xpath(xpath)
                self.webDriver.find_element_by_xpath(xpath).click()
            except:
                print("Exception: While clicking Industries button on main page during {} phase".format(i))

            try:
                xpath = "//ul[@data-test='secnav-list']//child::a"
                self.wait_by_xpath(xpath)
                xpath = xpath + '[@title = \'' + i + '\']'
                self.webDriver.find_element_by_xpath(xpath).click()
            except:
                print("Exception: While clicking {} industry".format(i))

            print("Scraping stocks in {} industry".format(i))

            xpath = "//table[@class='W(100%)']//child::a"
            self.wait_by_xpath(xpath)
            self.extract_stocks(xpath)




c = Crawler()
c.crawl('http://www.finance.yahoo.com')
