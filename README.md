
# SEC Equity Analysis

This project downloads scraped 10-Q and 10-K files from the SEC website, conducts VADER sentiment analysis on them with a finance dictionary, calculates the residual of the filing's sentiment based on its length, and then buys or shorts equities based off of those residuals. 

My rudimentary algorithm shorted any stock for the three-month period following any 10-Q filing that had a residual less than 1.5 standard deviations below the predicted residual. 

Over the period from January 30, 1995 to November 30, 2019 this algorithm, applied to a uniform bucket of the DOW Jones, **returned 13.11% annually**. 

The return looks promising, but the method has complications: 
- Changes in management can greatly affect the style, length, and sentiment of filings
- Scraping is imperfect and few filings have more text than just the MDA
- VADER sentiment analysis is less accurate than newer techniques, especially without a robust and accurate dictionary
- 10-Q Sentiment Residuals showed less length dependence than the Sentiment mean and sum; however, a more robust statistical technique would be preferable.  

10-Q 

## Getting Started

### Prerequisites

Python 3.7 or higher.
Packages: 
- Infrastructure: anaconda, os, string
- Analysis: pandas, numpy, sci-kit learn, nltk, html2text
- Data Acquisition: edgar, beautiful soup, re, pandas datareader
- Visualization: matplotlib. 

### Installing

Run "git clone URL" in terminal to install the repository on your computer. Open the main directory in any IDE. 

### Some Visualizations

<p align="center">

<img src="images/MMMmeasures.jpeg" alt="Default Login Screen" width="600"/>
<img src="images/MMMresidual.jpeg" alt="Default Login Screen" width="600"/>
<img src="images/MMMstock.jpeg" alt="Default Login Screen" width="600"/>
<img src="images/SNAPstock.jpeg" alt="Default Login Screen" width="600"/>
<img src="images/CATstock.jpeg" width="600"/>

</p>



## Built With

* [PyCharm](https://www.jetbrains.com/pycharm/) - The Python IDE
