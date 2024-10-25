# 760k-Car-Owners-Nationwide-China
# Nationwide Car Owner Data Translation and Cleaning

This project performs data translation, cleaning, and formatting on a dataset containing nationwide car owner information from China. The primary objective is to translate text fields, clean up special characters, and format the data for further analysis.

## Features
- **Translation of Column Headers and Rows**: Translates the headers and the first five rows of the CSV file using Google Translate.
- **Data Cleaning**: Removes special characters, empty columns, and missing values; combines address fields; and drops unnecessary columns.
- **File Output**: Saves both the cleaned data and rows with missing values to separate CSV files for further analysis.

## Setup

To run this project, you need Python with the following libraries installed:
```bash
!pip install pandas
!pip install googletrans==3.1.0a0
