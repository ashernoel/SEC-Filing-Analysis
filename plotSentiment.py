

import pandas as pd
import ast
import matplotlib.pyplot as plt
import pandas_datareader.data as web
from datetime import datetime
import numpy as np
from sklearn.linear_model import LinearRegression
import csv


# This is the main function
def plotSentiment(ticker, filingType, startTime, endTime):

    # Read in the data and define initial variables
    SECInfo = pd.read_csv("sec_processed_filings/" + ticker + "-SEC-Information.csv")
    minTime = str(SECInfo["Filing Date"].min())

    sums = {}

    times = []
    sumss = []
    means = []
    lens = []
    for item, row in SECInfo.iterrows():

        row2 = ast.literal_eval(row["MDA Sentiment Analysis"])
        if row["Filing Type"] == filingType:
            times.append(convertDate(str(row["Filing Date"])))
            means.append(np.mean(row2))
            sumss.append(sum(row2))
            lens.append(len(row2))

    # Begin plotting data to check for outliers
    df_a = pd.DataFrame({"length": lens, "sums": sumss})
    fig = plt.figure()
    fig.suptitle(ticker)
    plt.subplot(2, 2, 3)
    plt.title("Length vs Mean Sentiment")
    plt.plot(lens, means, "go")
    plt.subplot(2, 2, 2)
    plt.title("Summed Sentiment vs Time")
    plt.plot(times, sumss, "ro")
    plt.subplot(2, 2, 1)
    plt.title("Mean Sentiment vs Time")
    plt.plot(times, means, "ro")
    plt.subplot(2, 2, 4)
    plt.title("Length vs Summed Sentiment")
    plt.plot(lens, sumss, "bo")
    plt.show()

    # Conduct Linear Regression the 10Q sentiments vs Length
    regressor = LinearRegression()
    regressor.fit(df_a[['length']], df_a[['sums']])  # training the algorithm

    # Store the residuals of the 10Q in two formats.
    residuals = []
    for index, item in enumerate(sumss):
        residuals.append(item - regressor.coef_[0][0]*lens[index] - regressor.intercept_[0])
        sums[times[index]] = item - regressor.coef_[0][0]*lens[index] - regressor.intercept_[0]

    # Get the stock data over time using the correct formats
    if startTime == "":
        start = datetime(int(minTime[0:4]), int(minTime[5:7]), int(minTime[-2:]))
    else:
        start = datetime(int(startTime[0:4]), int(startTime[5:7]), int(startTime[-2:]))
    end = datetime(int(endTime[0:4]), int(endTime[5:7]), int(endTime[-2:]))
    df_equity = web.DataReader(ticker, 'yahoo', start, end)
    stockTimes = []
    stockValues = []
    for item, row in df_equity.iterrows():
        stockTimes.append(convertDate(str(item)[0:10]))
        stockValues.append(row["Close"])

    # Plot the residual data over time alone first
    lists = sorted(sums.items())  # sorted by key, return a list of tuples
    x, y = zip(*lists)
    fig = plt.figure()
    plt.subplot(2, 1, 1)
    plt.title(ticker + ": Residual Sentiment vs Time")
    plt.plot(x, y, "go")
    plt.subplot(2, 1, 2)
    plt.title(ticker + ": Residual Sentiment vs Length")
    plt.plot(lens, residuals, "ro")
    plt.show()

    # Plot the residual and stock together on the same graph!
    fig, ax1 = plt.subplots()
    if startTime != "":
        plotTimes = [i for i in lists if i[0] >= convertDate(startTime)]
        x, y = zip(*plotTimes)
    df_residualsOld = pd.DataFrame({"Time": x, "Sentiment": y})
    df_residuals = reject_outliers(df_residualsOld)
    ax1.plot(df_residuals["Time"].tolist(), df_residuals["Sentiment"].tolist(), 'bo')
    linearRegression = LinearRegression()
    linearRegression.fit(df_residuals[["Time"]], df_residuals[["Sentiment"]])
    y_pred = linearRegression.predict(df_residuals[["Time"]])
    ax1.plot(df_residuals[["Time"]], y_pred, color='blue', linewidth=3)
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Sentiment', color='b')
    plt.title(ticker + " Stock Price and " + filingType + " Sentiment Residual")
    ax2 = ax1.twinx()
    ax2.plot(stockTimes, stockValues, 'r-')
    ax2.set_ylabel('Stock Price', color='r')
    fig.tight_layout()
    plt.show()

    # Calculate the returns from this individual stock and add it to a CSV
    returns = calculateReturns(df_residuals, linearRegression, stockTimes, stockValues)
    with open('tradingStrategyResults.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow([ticker, startTime, endTime, returns[0], returns[1]])

# Self explanatory function
def convertDate(YYYYMMDD):
    year = YYYYMMDD[0:4]
    day = str(int(((int(YYYYMMDD[5:7])-1)*30 + int(YYYYMMDD[-2:])))/365)[1:]
    return round(float(year + day) + 0.15, 2)

# Massive outliers are removed from the DataFrame
def reject_outliers(data):
    u = np.mean(data["Sentiment"])
    s = np.std(data["Sentiment"])
    data_filtered = data[(data["Sentiment"] > (u-5*s)) & (data["Sentiment"] < (u+5*s))]
    return data_filtered

def calculateReturns(residuals, regression, stockTimes, stockValues):

    # Initial investment
    startValue = 100

    buy = False
    short = False

    u = np.mean(residuals["Sentiment"])
    s = np.std(residuals["Sentiment"])

    # For each filing, if the residual is > 1.5 SD under the residual, short the stock over the next timeframe.
    # Otherwise, buy. This is a sentiment driven strategy that mostly checks for large outliers.

    for item, row in residuals.iterrows():
        if item == 0:
            oldTime = row["Time"]
            veryOldTime = oldTime

        if buy or short:

            try:
                sellTime = stockTimes.index(row["Time"])
                buyTime = stockTimes.index(oldTime)
            except ValueError:
                try:
                    sellTime = stockTimes.index(row["Time"] + 0.01)
                    buyTime = stockTimes.index(oldTime + 0.01)

                except ValueError:
                    sellTime = stockTimes.index(row["Time"] - 0.01)
                    buyTime = stockTimes.index(oldTime - 0.01)

            sellValue = stockValues[sellTime]
            buyValue = stockValues[buyTime]

            if buy:
                returnPercentage = sellValue/buyValue
                buy = False
            if short:
                returnPercentage = buyValue/sellValue
                short = False


            startValue = startValue * returnPercentage

        res = row["Sentiment"] - regression.coef_[0][0]*row["Time"] - regression.intercept_[0]


        if res > -1.5*s:
            buy = True
            oldTime = row["Time"]
        elif res < -1.5*s:
            short = True
            oldTime = row["Time"]
        else:
            continue

    # This if statement accounts for the very last interval of time
    if buy or short:
        try:
            buyTime = stockTimes.index(oldTime)
        except ValueError:
            try:
                buyTime = stockTimes.index(oldTime + 0.01)

            except ValueError:
                buyTime = stockTimes.index(oldTime - 0.01)
        sellValue = stockValues[-1]
        buyValue = stockValues[buyTime]
        if buy:
            returnPercentage = sellValue / buyValue
        if short:
            returnPercentage = buyValue / sellValue
        startValue = startValue * returnPercentage

    # Print and return results
    print("Strategy: Long/Short when StDev")
    print("Sentiment Driven: " + str(startValue))
    print("Passive: " + str(100*stockValues[-1]/stockValues[0]))
    return [startValue, 100*stockValues[-1]/stockValues[0]]

# Print the results from the CSV after a batch of stocks is inputted
def summarizeResults():

    tradingResults = pd.read_csv("tradingStrategyResults.csv")
    endSent = tradingResults["sentiment strategy"].mean()
    endPass = tradingResults["passive strategy"].mean()
    print("Sentiment Average return: " + str(endSent))
    print("Passive average return: " + str(endPass))

    # Print the annualized average over the time period
    years = - convertDate(tradingResults['start'].iloc[0]) + convertDate(tradingResults['end'].iloc[0])
    annualizedReturnSent = (((endSent)/100) ** (1/years) - 1)*100
    annualizedReturnPassive = (((endPass)/100) ** (1/years) - 1)*100
    print("Annualized Return Sentiment: " + str(annualizedReturnSent))
    print("Annualized Return Passive: " + str(annualizedReturnPassive))


files = ["VZ", "UNH", "UTX", "TRV", "PG", "PFE", "NKE", "MRK", "MCD", "JPM", "JNJ", "INTC", "IBM", "HD", "GS", "XOM", "KO", "CSCO", "CVX", "CAT", "BA", "AAPL", "AXP", "MMM"]

for company in files:
     plotSentiment(company, "10-Q", "1995-01-30", "2019-11-30")

summarizeResults()