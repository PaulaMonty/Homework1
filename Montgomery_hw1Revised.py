# -*- coding: utf-8 -*-
"""
Created on Mon Feb  4 13:31:05 2019
Advanced Python Homework 1
Author: Paula Montgomery

Revised 24 Feb 2019 to include the classes ValidDate and SaveFile
"""
#  Import all required modules for error handling, files, and date.
import requests
import json
import csv
import os
import datetime
# API key in a module to keep key hidden.  It is commented out and the demo 
# is used.  To use NASAkey uncoment from_NASAkey import APIkey and comment
# out APIkey = 'DEMO_KEY'

#from _NASAkey import APIkey

#  NASA provides a demo API key for instructional purposes.  
#  It is used here for simplicity.

APIkey = 'DEMO_KEY'
class ValidDate:
    '''This class checks user input for a valid date within the date range.'''

    def __init__(self, date_string):
        self.date_string = date_string
    #  While loop to ask for user input and varify input meets parameters.

    def validation_loop():
        y = True
        while y is True:
            date = ValidDate.valid_date()
            if isinstance(date, datetime.datetime) is True:
                x = ValidDate.date_range(date)
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


class SaveFile:
    '''This class saves the data to a JSON file.  If none is found, a file
    will be created.'''

    def __init__(self, ah):
        self.ah = ah

    # Function to access json data and displays the dictionary values.
    def json_data(self):
        #  Global variable for name of text file where data is stored.
        filename = 'APOD_data.txt'
        APOD = json.loads(requests.get(self).text)
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


#  Main function.  Asks users if they want to continue looking for APOD.
def main():
    print('''Every day NASA shares an Astronomy Picture of the\n
      Day (APOD) along with a brief explanation written by\n
      two professors of astronomy, Robert Nemiroff (MTU)\n
      and Jerry Bonnell (UMCP).  This program uses an API\n
      to retrieve the data regarding the APOD.  You will be\n
      asked to enter a date starting 1995-06-16 to today.\n
      Please use the yyyy-mm-dd format.\n''')
    while True:
        again = input('''Do you want to look for an APOD to add to your file? Enter y/n: ''')
        if again == 'n':
            print('You found some amazing pictures!  See you next time!')
            return
        elif again == 'y':
            date = ValidDate.validation_loop()
# Creates the url for retrieving the APOD data by concantonating
# the static information with the API key and user input date.
            APOD_https = 'https://api.nasa.gov/planetary/apod?api_key='+APIkey+'&date='+date
            SaveFile.json_data(APOD_https)
        else:
            print('Please enter either y or n.')


if __name__ == '__main__':
    main()
