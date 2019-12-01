## DATA ACQUISITION 
# Import the Data from the CSV that I made using Python in the same directory
f <- file.choose()
data = read.csv(f, header = TRUE)

# Download and install XGBoost upon first run: install.packages("xgboost")
# XGBoost is short for eXtreme Gradient Boosting and will find 
# a relation (or not) between sentiment and stock price
library(xgboost)

# Downlaod and install tidyverse upon first run: install.packages("tidyverse")
# Tidyverse has utility functions that help with data cleaning
library(tidyverse)

# Set a random seed and shuffle the dataframe 
set.seed(1234)
data <- data[sample(1:nrow(data)), ];


## DATA CLEANING:
# We will have to: 
# 1) Remove information about the target variable from the training data
# 2) Remove redundant information
# 3) Convert categorical information (like "Filing Year") to a numeric format
# 4) Split dataset into testing and training subsets
# 5) Convert the cleaned dataframe to a Dmatrix, per XGBoost specifications

# 1a) Remove information about the target variable: stock values
data_stockValuesRemoved <- data %>%
  select(-Stock.Values)

# 1b) Remember the target variable for training and testing purposes 
stockValues <- data %>%
  select(Stock.Values)

# Check to see the stock values and the removed stock values from the dataframe
head(stockValues)

# 2) Remove redundant information 

# Remove non-numeric columns from the dataframe 
data_numeric <- data_stockValuesRemoved %>%
  select(-MDA.Sentiment.Analysis) %>%
  select(-Net.Income) %>%
  select(-Filing.Year) %>%
  select(-Filing.Type) %>%
  select(-Unnamed) %>%
  select(-X);

# Remove 10-K's to only focus on 10-Qs
subset(data_numeric, Filing.Type!="10-K");

  
# 3) Convert the Filing.Date to a number
YYYYMMDD_to_decimalDate <- function(YYYYMMDD) {
  
  # Convert the YYYY-MM-DD format to a usable string
  year <- as.integer(substr(YYYYMMDD, start=1, stop=4));
  month <- as.integer(substr(YYYYMMDD, start=6, stop=7));
  day <- as.integer(substr(YYYYMMDD, start=9, stop=10));
  
  # Convert the month and day into an approximate demical representing
  # the progress through the year. 
  decimalDate <- ((month - 1)*30 + day)/365.0 
  
  # Return the time so June 15, 2019 => 2019.5 
  year + decimalDate;
  
}

## Apply the function to the column and update the original times
convertedTimes <- sapply(data_numeric$Filing.Date, YYYYMMDD_to_decimalDate);
data_numeric$Filing.Date <- convertedTimes;

head(data_numeric)

## Reduce the size of the dates so that they are a lot smaller
## This helps regression
## improve the XGBoost model
for(i in 1:nrow(data_numeric)) {
  row <- data_numeric[i,]
  data_numeric[i,"Filing.Date"] <- row$Filing.Date - 2000
}

head(data_numeric)

# 4) Split the dataset!

# Convert the dataframes to tablesa
data_matrix <- data.matrix(data_numeric)
data_labels <- data.matrix(stockValues)

# Split the Data into a 70/30 split using our new function
getNUMEntries <- function(dataframe) {
  round(nrow(dataframe) * 0.7)
}

numberOfTrainingEntries <- getNUMEntries(stockValues)

# Get the Training Data
train_data <- data_matrix[1:numberOfTrainingEntries,]
train_labels <- data_labels[1:numberOfTrainingEntries]

# Get the Testing Data
test_data <- data_matrix[-(1:numberOfTrainingEntries),]
test_labels <- data_labels[-(1:numberOfTrainingEntries)]

# 5) Convert the cleaned matrix to a DMatrix
train_data
test_data
train_labels
test_labels
dtrain <- xgb.DMatrix(data = train_data, label= train_labels)
dtest <- xgb.DMatrix(data = test_data, label= test_labels)

#### TRAIN THE MODEL
model <- xgboost(data = dtrain, # the data   
                 nround = 4, # max number of boosting iterations
                 objective = "reg:linear")  # the objective functi

predictions <- predict(model, dtest)

#### Visualize the model

# Plot a diagram of how much each feature contributes to the model. 
# A high number next to the feature indicates high contribution!
# INSTALL PACKAGE install.packages("DiagrammeR")
xgb.plot.multi.trees(feature_names = names(dtrain), 
                     model = model)

# Get and plot information about the relative importance of each feature
importance_matrix <- xgb.importance(names(dtrain), model = model)

xgb.plot.importance(importance_matrix)

# Install and use GGplot
library(ggplot2)
# install.packages("Ckmeans.1d.dp")
xgb.ggplt<-xgb.ggplot.importance(importance_matrix)
# Make the feature importance graph pretty! 
xgb.ggplt+theme( text = element_text(size = 20),
                 axis.text.x = element_text(size = 15, angle = 45, hjust = 1))


