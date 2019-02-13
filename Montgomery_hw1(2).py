# -*- coding: utf-8 -*-
"""
Created on Mon Feb  4 13:31:05 2019
Advanced Python Homework 1
Author: Paula Montgomery
"""
#  Import all required modules for error handling, files, and date.
import requests
import json
import csv
import os
import datetime

#  By placing the API key in a variable it is easier to replace the API key as 
# needed.
API_key = 'iakCg0OU2ILRUE3tsCOywrBWSwRblVubInLFm5ib'
#  Global variable for name of text file where data is stored.
filename = 'APOD_data.txt'


#  Function to print instructions
def instructions():
    print('''Every day NASA shares an Astronomy Picture of the\
          Day (APOD) along with a brief explanation written by\
          two professors of astronomy, Robert Nemiroff (MTU)\
          and Jerry Bonnell (UMCP).  This program uses an API\
          to retrieve the data regarding the APOD.  You will be\
          asked to enter a date starting 1995-06-16 to today.\
          Please use the yyyy-mm-dd format.\n''')


# Function to ensure user entered date is a date and format input as date .
def valid_date():
    date_format = '%Y-%m-%d'
    date_string = input('What date would you like to see the APOD? (yyyy-mm-dd) ')
    try:
        date_obj = datetime.datetime.strptime(date_string,date_format)
        return date_obj
    except ValueError:
        print('You did not enter a valid date.  Please try again.')


#  Function to varify user entered date is in range.
def date_range(d):
    date_format = '%Y-%m-%d'
    start = '1995-06-16'
    end = datetime.datetime.today()
    start = datetime.datetime.strptime(start, date_format)
    compare = start <= d <= end
    if compare is True:
        x = 0
        return x
    else:
        x = 1
        return x


#  Try Except to handle errors associted with the url.
def error_check(h):
    try:
        r = requests.get(h,timeout=3)
        r.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        print("Http Error:", errh)
        print('You did not input a valid date.')
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print("OOps: Something Else", err)


# Function to access json data and displays the dictionary values.
def json_data(ah):
    APOD = json.loads(requests.get(ah).text)
    for key, val in APOD.items():
        print('\n')
        print(key, val)
    print('\n')
    print('To view the image, copy the hdurl or url value into your browser.')
# If not exists, creates a file named APOD_data in the current directory.  Then
# it appends the data retrieved to the csv file using the DictWriter method.
# The text file has a header row followed by rows of data.  The file can be
# imported into Excel as a csv for easier viewing.
    file_exists = os.path.isfile(filename)
    with open(filename, 'a') as fh:
        headers = ['copyright','date','explanation',
                   'hdurl','media_type','service_version','title','url']
        writer = csv.DictWriter(fh, delimiter=',',lineterminator='\n', 
                                fieldnames=headers)
        if not file_exists:
            writer.writeheader()
            writer.writerow(APOD)
        else:
            writer.writerow(APOD)


#  While loop to ask for user input and varify input meets parameters.
def validation_loop():
    y = True
    while y is True:
        date = valid_date()
        if isinstance(date, datetime.datetime) is True:
            x = date_range(date)
            if x != 0:
                print('You slected a date out of range.  Please choose a date 1995-06-16 to today.')
            elif x == 0:
                date = str(date)
                date = date[:10]
                y = False
                return date
                break
        elif isinstance(date, datetime.datetime) is False:
            print('This is an invalid date.')


#  Main function.  Asks users if they want to continue looking for APOD.
def main():
    while True:
        again = input('''Do you want to look for an APOD to add to your file? Enter y/n: ''')
        if again == 'n':
            print('You found some amazing pictures!  See you next time!')
            return
        elif again == 'y':
            date = validation_loop()
# Creates the url for retrieving the APOD data by concantonating
# the static information with the API key and user input date.
            APOD_https = 'https://api.nasa.gov/planetary/apod?api_key='+API_key+'&date='+date
            error_check(APOD_https)
            json_data(APOD_https)
        else:
            print('Please enter either y or n.')


if __name__ == '__main__':
    instructions()
    main()
