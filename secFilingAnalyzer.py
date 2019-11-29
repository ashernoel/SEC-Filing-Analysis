from sec_edgar_downloader import Downloader
import html2text
import pandas as pd
import os
import re
import string

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

                    if "financial statements and supplementary data" in line.lower().rstrip() or "statements and supplementary" in line.lower().rstrip():

                        flag = False

                    # Get the time of the filing
                    if "conformed period of report" in line.lower().rstrip():
                        filingDate = line.lower().split("report: ", 1)[1][:8]


                wfile.close()
                w2.close()

                placeholder = True
                netIncome = True

                SECInfo = SECInfo.append({"Filing Type": "10-K", "Filing Year": year, "Filing Date": filingDate, "Net Income": netIncome, "MDA Sentiment Analysis": placeholder}, ignore_index=True)

            except NotImplementedError:
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

                flag = False
                for line in w:


                    if flag or "s discussion and analysis of" in line.lower().rstrip() or "management's discussion and analysis" in line.lower().rstrip():

                        if len(line) > 20 and count_punct(line) < 5 and " " in line:
                            w2.write(line)
                        flag = True

                    if "controls and procedures" in line.lower().rstrip():

                        flag = False

                    # Get the time of the filing
                    if "conformed period of report" in line.lower().rstrip():
                        filingDate = line.lower().split("report: ", 1)[1][:8]

                wfile.close()
                w2.close()
                SECInfo = SECInfo.append(
                    {"Filing Type": "10-Q", "Filing Year": year, "Filing Date": filingDate, "Net Income": netIncome,
                     "MDA Sentiment Analysis": placeholder}, ignore_index=True)

            except NotImplementedError:
                w.close()
                print("not implemented error for " + year)
                continue



            continue
        else:
            continue


getFilings("SNAP")