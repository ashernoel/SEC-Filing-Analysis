
# SEC Equity Analysis

This project scrapes 10-Q and 10-K files from the SEC website, conducts VADER sentiment analysis on them with a dictionary of financial terms, calculates the residual of the filing's sentiment compared to the predicted sentiment based on its length, and then buys or shorts equities based off of those residuals. 

My rudimentary algorithm shorted any stock following any 10-Q filing that had a residual less than 1.5 standard deviations below the predicted residual and bought the stock otherwise. 

The algorithm **returned 12.68% annually** when applied to a uniform bucket of the DOW Jones over the period from January 30, 1995 to November 30, 2019.

The return looks promising, but the method has complications: 
- Changes in management can greatly affect the style, length, and sentiment of filings; 
- The scraping is imperfect and a few filings have more text than just the MDA; 
- VADER sentiment analysis is less accurate than newer techniques, such as those utilizing BERT, especially without a robust and accurate dictionary; and
- 10-Q Sentiment Residuals showed less length dependence than the Sentiment mean and sum; however, a more robust statistical technique would be preferable.  

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
