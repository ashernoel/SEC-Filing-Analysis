from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, WebDriverException

import pandas as pd
import re
import time

URL = 'http://markets.ft.com/research/Browse-Companies/Technology/Software-and-Computer-Services'


def getCompanies(URL, industry_name):

    # Boot up the Selenium WebDriver with the correct URL in Safari
    browser = webdriver.Safari()
    browser.get(URL)
    browser.implicitly_wait(10)

    # Create dataframe to store name, Ticker, and exchange of stock.
    industry = pd.DataFrame(columns=["Company", "Ticker", "Exchange"])

    # For each page while next button is possible, click it!
    while True:

        # Get a list of all the elements with the correct class.
        data = browser.find_elements_by_class_name('company-link')

        # Get the names, Tickers, and stock exchange of these companies.
        for company in data:
            link = company.get_attribute("href")
            exchange = link.rsplit(':', 1)[1]
            result = re.search('s=(.*):', link)
            ticker = result.group(1)

            print(company.text)
            # Add the exchange, result, and company name to the industry DataFrame
            industry = industry.append({"Company": company.text, "Ticker": ticker, "Exchange": exchange}, ignore_index=True)



        try:
            elem = browser.find_element_by_xpath("//div[contains(@class, 'wsod-icon wsod-icon-v wsod-icon-paging-next-active')]")
        except NoSuchElementException:
            break  # no more pages

    # Save the industry to a CSV
    industry.to_csv(f'{industry_name} companies.csv')

    # Close the selenium file at the end. This stops the session.
    browser.close()

# Software industry
getCompanies('http://markets.ft.com/research/Browse-Companies/Technology/Software-and-Computer-Services', "Software")

# Mining industry
#getCompanies("http://markets.ft.com/research/Browse-Companies/Basic-Materials/Mining", "Mining")

# Manufacturing industry
#getCompanies("http://markets.ft.com/research/Browse-Companies/Industrials/Construction-and-Materials", "Manufacturing")