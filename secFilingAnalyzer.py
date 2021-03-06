from sec_edgar_downloader import Downloader
import html2text
import pandas as pd
import os
import re
import string
import csv

from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA

# Download VADER upon first run
# import nltk
# nltk.download('vader_lexicon')

# Import financial dictionarities
with open('Financial Dictionary/negative_words.csv', mode='r') as infile:
    reader = csv.reader(infile)
    negative_words = {rows[0].lower():int(rows[1]) for rows in reader}
with open('Financial Dictionary/positive_words.csv', mode='r') as infile:
    reader = csv.reader(infile)
    positive_words = {rows[0].lower():int(rows[1]) for rows in reader}

# Update VADER with new dictionaries
sid = SIA()
sid.lexicon.update(positive_words)
sid.lexicon.update(negative_words)

# A function to make sure that there is not too much punctuation in a line from the MDA
def count_punct(text):
    if text.strip() == "":
        return 0
    count = sum([1 if char in string.punctuation else 0 for char in text ])
    spaces = text.count(" ")
    total_chars = len(text) - spaces
    return round(count / total_chars, 3)*100

# This is the main function
def getFilings(ticker):

    # Get all 10-K and 10-Q filings for a ticker
    dl = Downloader(os.getcwd())
    dl.get_10k_filings(ticker)
    dl.get_10q_filings(ticker)

    # Get the directories of the newly added files
    directoryK = os.getcwd() + "/sec_edgar_filings/" + ticker + "/10-K"
    directoryQ = os.getcwd() + "/sec_edgar_filings/" + ticker + "/10-Q"

    # Create dataframe to store information scraped from filings
    SECInfo = pd.DataFrame(columns=["Filing Type", "Filing Year", "Filing Date", "Net Income", "MDA Sentiment Analysis"])

    # For each new text file, go through and CLEAN IT!
    for filename in os.listdir(directoryK):
        if filename.endswith(".txt"):

            # Make a new cleaned file
            year = re.search('-(.*)-', filename).group(1)
            html = open(directoryK + "/" + filename)
            f = html.read()
            name = directoryK + "-cleaned" + "/" + ticker + "-" + year + "-" + "10K.txt"
            os.makedirs(os.path.dirname(name), exist_ok=True)

            # Store the sentiment of each word as the scraper goes through the MDA
            sentiment = []

            # If there is an error, move onto the next file.
            try:

                # Convert the HTML to a readable format in the first file
                w = open(name, "w")
                w.write(html2text.html2text(f))
                html.close()
                name2 = directoryK + "-MDA" + "/" + ticker + "-" + year + "-" + "10K-MDA.txt"
                os.makedirs(os.path.dirname(name2), exist_ok=True)
                w.close()

                # Convert the Readable Format to MDA in the second file
                wfile = open(name, "r")
                w = wfile.readlines()
                w2 = open(name2, "w")

                # For each line, check to see if it is the start of an MDA section or the start of the next section.
                flag = False
                for line in w:

                    if flag or "discussion and analysis of" in line.lower().rstrip() or "management's discussion and analysis" in line.lower().rstrip():

                        # Make sure the line is legitimate and not all punctuation before adding
                        if len(line) > 20 and count_punct(line) < 4 and " " in line:
                            w2.write(line)
                        flag = True

                        # Conduct sentiment analysis
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

                # This is a placeholder value that I did not get to resolve
                netIncome = True

                try:
                    SECInfo = SECInfo.append({"Filing Type": "10-K", "Filing Year": year, "Filing Date": filingDate, "Net Income": netIncome, "MDA Sentiment Analysis": sentiment}, ignore_index=True)

                except UnboundLocalError:
                    continue
            except (NotImplementedError, UnicodeEncodeError) as error:
                print("not implemented error for " + year)
                continue

            continue
        else:
            continue

    # This is the same loop as above except for 10-Q filings instead of 10-Ks. See thsoe comments.
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

    # Convert the large DataFrame we have made to a CSV for later use.
    SECInfo.to_csv("sec_processed_filings/" + ticker + "-SEC-Information.csv")

