from sec_edgar_downloader import Downloader
import html2text
import pandas as pd
import os
import re
import string
import csv

from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA

# import nltk
# nltk.download('vader_lexicon')

with open('Financial Dictionary/negative_words.csv', mode='r') as infile:
    reader = csv.reader(infile)
    negative_words = {rows[0].lower():int(rows[1]) for rows in reader}

with open('Financial Dictionary/positive_words.csv', mode='r') as infile:
    reader = csv.reader(infile)
    positive_words = {rows[0].lower():int(rows[1]) for rows in reader}

sid = SIA()
sid.lexicon.update(positive_words)
sid.lexicon.update(negative_words)

def count_punct(text):
    if text.strip() == "": # To take of care of all space input
        return 0
    count = sum([1 if char in string.punctuation else 0 for char in text ])
    spaces = text.count(" ") # Your error is here, Only check for 1 space instead of 3 spaces
    total_chars = len(text) - spaces

    return round(count / total_chars, 3)*100



def getFilings(ticker):

    dl = Downloader(os.getcwd())

    # Get all 10-K filings for a ticker
    dl.get_10k_filings(ticker)

    # Get all 10-Qs for the same stock
    dl.get_10q_filings(ticker)

    # Get directories of files
    directoryK = os.getcwd() + "/sec_edgar_filings/" + ticker + "/10-K"
    directoryQ = os.getcwd() + "/sec_edgar_filings/" + ticker + "/10-Q"

    # Create dataframe to store information scraped from filings
    SECInfo = pd.DataFrame(columns=["Filing Type", "Filing Year", "Filing Date", "Net Income", "MDA Sentiment Analysis"])
    print(directoryK)

    for filename in os.listdir(directoryK):
        if filename.endswith(".txt"):

            year = re.search('-(.*)-', filename).group(1)
            html = open(directoryK + "/" + filename)
            f = html.read()
            name = directoryK + "-cleaned" + "/" + ticker + "-" + year + "-" + "10K.txt"

            os.makedirs(os.path.dirname(name), exist_ok=True)

            sentiment = []

            try:
                w = open(name, "w")

                w.write(html2text.html2text(f))
                html.close()

                name2 = directoryK + "-MDA" + "/" + ticker + "-" + year + "-" + "10K-MDA.txt"
                os.makedirs(os.path.dirname(name2), exist_ok=True)
                w.close()

                wfile = open(name, "r")
                w = wfile.readlines()

                w2 = open(name2, "w")

                flag = False
                for line in w:


                    if flag or "discussion and analysis of" in line.lower().rstrip() or "management's discussion and analysis" in line.lower().rstrip():

                        if len(line) > 20 and count_punct(line) < 4 and " " in line:
                            w2.write(line)
                        flag = True

                        pol_score = sid.polarity_scores(line)

                        sentiment.append(pol_score["compound"])

                    if "financial statements and supplementary data" in line.lower().rstrip() or "statements and supplementary" in line.lower().rstrip():

                        flag = False

                    # Get the time of the filing
                    if "conformed period of report" in line.lower().rstrip():
                        filingDateRaw = line.lower().split("report: ", 1)[1][:8]
                        filingDate = filingDateRaw[0:4] + "-" + filingDateRaw[4:6] + "-" + filingDateRaw[-2:]


                wfile.close()
                w2.close()

                netIncome = True

                SECInfo = SECInfo.append({"Filing Type": "10-K", "Filing Year": year, "Filing Date": filingDate, "Net Income": netIncome, "MDA Sentiment Analysis": sentiment}, ignore_index=True)

            except (NotImplementedError, UnicodeEncodeError) as error:
                print("not implemented error for " + year)
                continue

            continue
        else:
            continue

    for filename in os.listdir(directoryQ):
        if filename.endswith(".txt"):

            year = re.search('-(.*)-', filename).group(1)
            html2 = open(directoryQ + "/" + filename)
            f = html2.read()

            name = directoryQ + "-cleaned" + "/" + ticker + "-" + year + "-" + "10Q.txt"
            print(name)

            flag = False

            os.makedirs(os.path.dirname(name), exist_ok=True)
            w = open(name, "w")

            try:
                w.write(html2text.html2text(f))
                html2.close()

                name2 = directoryQ + "-MDA" + "/" + ticker + "-" + year + "-" + filename[14:20] + "-10Q-MDA.txt"
                os.makedirs(os.path.dirname(name2), exist_ok=True)
                w.close()

                wfile = open(name, "r")
                w = wfile.readlines()

                w2 = open(name2, "w")

                sentiment = []

                flag = False
                for line in w:


                    if flag or "s discussion and analysis of" in line.lower().rstrip() or "management's discussion and analysis" in line.lower().rstrip():

                        if len(line) > 20 and count_punct(line) < 5 and " " in line:
                            w2.write(line)
                        flag = True

                        pol_score = sid.polarity_scores(line)
                        sentiment.append(pol_score["compound"])

                    if "controls and procedures" in line.lower() or "in witness whereof" in line.lower() or "item 4." in line.lower():
                        flag = False

                    # Get the time of the filing
                    if "conformed period of report" in line.lower().rstrip():
                        filingDateRaw = line.lower().split("report: ", 1)[1][:8]
                        filingDate = filingDateRaw[0:4] + "-" + filingDateRaw[4:6] + "-" + filingDateRaw[-2:]

                wfile.close()
                w2.close()
                SECInfo = SECInfo.append(
                    {"Filing Type": "10-Q", "Filing Year": year, "Filing Date": filingDate, "Net Income": netIncome,
                     "MDA Sentiment Analysis": sentiment}, ignore_index=True)

            except (NotImplementedError, UnicodeEncodeError) as error:
                w.close()
                print("not implemented error for " + year)
                continue

            continue
        else:
            continue

    SECInfo.to_csv("sec_processed_filings/" + ticker + "-SEC-Information.csv")


getFilings("DFS")

