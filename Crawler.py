
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
        self.wait = WebDriverWait(self.webDriver, 10)
        self.element_list = []
        self.s = Stocks.Stock()

    # This function waits for the given xpath to become visible and clickable
    def wait_by_xpath(self, xpath):
        self.wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
        self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))

    # This method loads the industry list with dictionaries [Title : href]
    # It takes the xpath as an argument from 'crawl' function
    def load_industries(self, xpath):
        print("Loading list of all industries...")
        self.element_list = []
        # Creates list of all web elements for each industry
        self.element_list = self.webDriver.find_elements_by_xpath(xpath)

        for i in self.element_list:
            title = i.get_attribute('title')
            href = i.get_attribute('href')
            key_val = {title: href}          # Create a dictionary
            self.industries.append(key_val)  # append it to the list

        print("Industries data updated.")

    # Extracts stocks information for a given file/Industry.
    # It takes offset as an argument which ensures that the header
    # is written only once in the file for multiple pages of stocks
    def extract_stocks(self, file, offset):
        print("Stock information being written to file : {}".format(file))

        # Create a file even if it does not exists (option a+)
        with open(file, 'a+') as f:
            # This xpath gives list of each row on the summary page of the selected industry
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

                # this will directly convert the Stock class object attributes into dictionary
                row_dict = self.s.__dict__
                # Writes dictionary into row in the file
                w = csv.DictWriter(f, row_dict.keys())
                if offset == 0:
                    w.writeheader()
                    offset += 1
                w.writerow(row_dict)

    # Starts crawling form the given homepage of Yahoo finance.
    # Collects all the industry details from the homepage
    # Clears all the contents from the output file directory, removes and recreates the directory
    # Creates csv file per industry in the output folder
    # Iterates through pages for each industry
    # Opens the first page of the industry, collects count of stocks
    # Iterates through each page in the industry until offset is more than the number of stocks captured
    def crawl(self, url):
        self.webDriver.maximize_window()
        self.webDriver.get(url)                 # open the homepage

        # Get the titles of all industries in yahoo finance and load it in the list
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

            # expects only one key as the industry name same a file name
            file = ''.join(list(i.keys()))
            #create full path of the output file for each industry
            #print("element is {}".format(file))
            file_nm = file + '.csv'
            script_dir = os.path.dirname(__file__)
            full_path = os.path.join(script_dir, output_dir, file_nm)

            href = i[file]

            offset = 0
            while True:
                # Ex: https://finance.yahoo.com/sector/financial?offset=0&count=200
                # Ex: https://finance.yahoo.com/sector/technology?offset=200&count=200
                href_itr = href + "?offset=" + str(offset) + "&count=200"
                self.webDriver.get(href_itr)
                self.extract_stocks(full_path, offset)

                if offset == 0:
                    # extract text label which shows total stocks
                    xpath = "//span[@class='Mstart(15px) Fw(500) Fz(s) Mstart(0)--mobp Fl(start)--mobp']//child::*"
                    textLable = self.webDriver.find_element_by_xpath(xpath).text
                    # third string in the label has the number of stocks
                    stocks_count = int(textLable.split(" ")[2])
                    print("{} has {} Stocks".format(file, stocks_count))
                    print("Scraping stocks in {} industry".format(file))

                offset = offset + 200

                if offset >= stocks_count:
                    break

if __name__ == "__main__":
    c = Crawler()
    c.crawl('http://www.finance.yahoo.com')
