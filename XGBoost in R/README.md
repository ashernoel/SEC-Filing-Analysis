

# SEC Equity Analysis

This project finds the relation between time-series stock price and sentiment analysis data from quarterly SEC 10-Q filings scaped and processed in a different Python program. It applies an eXtreme Gradient Descient Boost algorithm to the data visualized below and then predicts the stock price from sentiment analysis and time-series data. The R script then creates two visualizations summarizing the results and the relative importance of 1) time-series stock data and 2) the sentiment residuals in predicting stock price using the eXtreme Gradient Descent Boost's linear regression. 

## Getting Started

### Installing

Prerequisites: RStudio 

Download the files submitted in the Gradescope assignment. 
If R Markdown does not work at first, type #install.packages("rmarkdown") at the top and run the line. 

### Understanding the Directory

1) README.md: This file with installation instructions
2) RProject.rmd: The R Project's main file. Run the code by using the "Knit" button in RStudio
3) SNAP-SEC-Information.csv: This is the first data file. It is the default file in the R project. 
4) CAT-SEC-Information.csv: This is the second data file. You can change the R project to use this data in line 31. 
5) SNAPstockR.jpeg: This is the Pre-R Visualization that is shown below. 

### Pre-R Data Visualizations

<p align="center"><img src="SNAPstockR.jpeg" alt="Default Login Screen" width="600"/></p>

## Earned Points 

Basic Requirements (8/8):
(+2): "Topic is related to lienar algebra, real analysis, or multivariable calculus." Our project is related to both linear algebra and real analysis. XGBoost utilizes multivariate regression by minimizing the loss function (in other words, the difference between the predicted and actual stock prices). It relates to linear algebra because XGBoost utilizes a sparse matrix that lets the computations occur quickly. 
(+2): "the script is commented well enough to be reasonably self-explanatory (lines should be no longer than 80 characters wide)" There are many many comments and ample explanation throughout. 
(+2): "The script generates at least one nice-looking graphic": The script generates two pretty graphs, one of which utilizes ggplot2, the industry standard plotting package. 
(+2): "The script is uploaded before the due date, and both team members participate in the presentation": Both of these criteria are filled. 

Additional Points (11/11: 
(+1): "Project is related to a topic that you have studied in another course this term" In my statistics course, STAT 110, we learned about regression and minimizes the residuals through mean squared error, which is the technique that XGBoost uses for its loss function. 
(+1): "Uses an R function that has not appeared in any Math 23 lecture script": In line 107, we wrote a new function "YYYYMMDD_to_decimalDate" that has not appeared in any script. 
(+1): "Uses a random-number function and a for loop." Our random number function is on line 56-57 to scramble the data set and our for loop is on line 136-139
(+1): "Defines and uses at least two functions" Function 1 is on line 107-121, and function 2 is on 158-160
(+1): "Uses a permutation test, bootstrap, or other similar statistical technique": XGBoost is a state of the art statistical learning technique to understand datasets and make predictions based off of multivariate regression and the minimizization of a gradient mean squared error function. 
(+1): "Includes two related but distinct topics": It includes the topics of 1) sentiment analysis in the input file and then 2) time-series analysis using the XGBoost multivariate regression in the R script. This sentiment analysis used VADER sentiment analysis, as described in the RProject.rmd header and a dictionary of financial terms to, to get a residual sentiment analysis or deviation from the predicted total net sentiment based off of the length of the filing. The time-series analysis topic is the XGBoost algorithm.
(+1): "Delves into a new library/R package" We delve into many packages, most notable XGBoost. 
(+1): "Professional Looking software engineering": The R markdown script looks beautiful and the final visualization is made in accord with industry standards in the data science community. 
(+2): "Integrating well-writen LateX with R code in a final write-up via R markdown." Some nice LateX is on line 104 of the R markdown file, which includes our final-write up. 
(+1): "Having a 2 person team": Made by Asher Noel and Kat Zhang!

Impressing Course Staff (maximum of 3 points):
(+1): "Well, at least they can do something original in R."
(+2): "Let's put this on the website for next year"
(+3): "Let's present somethign like this in lecture next year"

Total points earned: Minimum(8 + 11 + impressing course staff points, 20) = **Minimum(19 + impressing course staff points, 20)**

## YouTube Link to Narrated Script


## Built With

* [PyCharm] - The Python IDE
* [RStudio] - The R IDE
