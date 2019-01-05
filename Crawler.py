
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

import Stocks
import csv
import os
import shutil


class Crawler:

    def __init__(self):
        self.webDriver = webdriver.Chrome()
        self.industries = []
        self.industries_href = []
        self.wait_df = 10
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
            title = i.get_attribute('title')
            href = i.get_attribute('href')
            key_val = {title: href}
            self.industries.append(key_val)

        # adding test breakpoint
        print("{}".format(self.industries))
        #self.industries = ['Technology']

    def extract_stocks(self, file, offset):

        print("Stock information being written to file : {}".format(file))
        #Create a file even if it doesnot exists (option a+)
        with open(file, 'a+') as f:

            #row_number = 1
            xpath = "//table[@class='W(100%)']//child::a"
            self.element_list = []
            self.wait_by_xpath(xpath)
            self.element_list = self.webDriver.find_elements_by_xpath(xpath)
            print("Generated element list from the stock table")
            print("Loading stock object from stock element details..")
            for e in self.element_list:
                self.s.ticker = e.text
                self.s.name = e.get_attribute('title')
                self.wait_by_xpath(xpath)

                # this will directly convert an class object attributes into dictionary
                row_dict = self.s.__dict__
                w = csv.DictWriter(f, row_dict.keys())
                if offset == 0:
                    w.writeheader()
                    offset += 1
                w.writerow(row_dict)
                #row_number += 1

            #print("{} rows writen to {}".format(row_number,file))




    def crawl(self, url):
        self.webDriver.maximize_window()
        self.webDriver.get(url)

        # Get the titles of all industries in yahoo finance
        self.webDriver.find_element_by_xpath("//a[@title='Industries']").click()

        xpath = "//ul[@data-test='secnav-list']//child::a"
        self.wait_by_xpath(xpath)
        self.load_industries(xpath)

        #Remove the output directory if it exists already and then create a new one
        output_dir = "OutputFiles"
        if os.path.exists(output_dir):
            print("found an existing {} directory".format(output_dir))
            print("{} directory will be removed along with its contents".format(output_dir))
            shutil.rmtree(output_dir)
        os.makedirs(output_dir)
        print("{} directory is created".format(output_dir))

        # iterate through pages for each industry
        for i in self.industries:

            file = ''.join(list(i.keys()))
            #create full path of the output file for each industry
            #print("element is {}".format(file))
            file_nm = file + '.csv'
            script_dir = os.path.dirname(__file__)
            full_path = os.path.join(script_dir, output_dir, file_nm)

            href = i[file]

            offset =0
            while True:
                href_itr = href + "?offset=" + str(offset) + "&count=200"
                self.webDriver.get(href_itr)
                self.extract_stocks(full_path, offset)

                if offset == 0:
                    xpath = "//span[@class='Mstart(15px) Fw(500) Fz(s) Mstart(0)--mobp Fl(start)--mobp']//child::*"
                    textLable = self.webDriver.find_element_by_xpath(xpath).text
                    stocks_count = int(textLable.split(" ")[2])
                    print("{} has {} Stocks".format(file, stocks_count))
                    print("Scraping stocks in {} industry".format(file))

                offset = offset + 200

                if offset >= stocks_count:
                    break



                # [div, mod] = divmod(stocks_count, 200)
                # print("Div : {} and Rem: {}".format(div, mod))

                # if mod != 0:
                #     itr = div
                # else:
                #     itr = div - 1

                # offset = 200
                # for i in range(0, itr):




            # try:
            #     xpath = "//a[@title='Industries']"
            #     self.wait_by_xpath(xpath)
            #     self.webDriver.find_element_by_xpath(xpath).click()
            # except:
            #     print("Exception: While clicking Industries button on main page during {} phase".format(i))
            #
            # try:
            #     xpath = "//ul[@data-test='secnav-list']//child::a"
            #     self.wait_by_xpath(xpath)
            #     xpath = xpath + '[@title = \'' + i + '\']'
            #     self.webDriver.find_element_by_xpath(xpath).click()
            # except:
            #     print("Exception: While clicking {} industry".format(i))

            # try:
            #     xpath = "//div[@data-test='select-container']"
            #     self.wait_by_xpath(xpath)
            #     self.webDriver.find_element_by_xpath(xpath).click()
            #     self.webDriver.find_elements_by_xpath()
            #     select_options = select_box.options
            #         #deselect_by_visible_text('Show 100 rows')
            #     print("Dropdown has {} options".format(select_options))
            # except:
            #     print("No drop downs")
            #     pass






c = Crawler()
c.crawl('http://www.finance.yahoo.com')
