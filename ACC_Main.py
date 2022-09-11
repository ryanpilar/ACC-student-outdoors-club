#!/usr/bin/env python
# coding: utf-8

# In[2]:

import urllib
import ACC_stylize

import numpy as np
import pandas as pd
import xml.dom.minidom
import ACC_AddressComplete
import ACC_inputBehaviours

from IPython.display import display
from IPython.display import clear_output

pd.set_option('display.max_columns', None)  
pd.set_option('display.expand_frame_repr', False)
pd.set_option('max_colwidth', None)

class correctACCsubmission():
    '''
    class correctACCsubmission is a tool that helps automate 
    the processes involved with ACC Group Submissions. It takes 
    information from an xcel sheet (a member form submission)and
    formats the data in a way that allows for an IMIS submission. 
    '''
    def __init__(self, Key):
        self.Key = Key

        self.template_pd = None
        self.original_pd = None
        self.template_fileName = None
        self.original_fileName = None

        self.quitting = False
        self.addressPrint = {}
        self.address_series = None             # pre AddressComplete converstion, a panda series
        self.convertedAddresses = None         # converted from AddressComplete, a panda dataframe
        
    def getACC_object(self):
        return self
        
    def importTemplate(self, fileName):
        '''
        takes in: a string, which will be an excel filename
        
        the Perfect_Template.xlsx is a heading only excel file
        that serves as an empty base template, that once filled,
        will be submitted to the IMIS database. The xlsx file is 
        imported, and a panda series is created
        
        returns: nothing, but updates self.template_pd     
        '''
        self.template_fileName = fileName
        self.template_pd = pd.read_excel(fileName)
    
    def importOriginal(self, fileName):
        '''
        takes in: a string, which will be excel filename
        
        the original_fileName.xlsx is a form filled out by an
        ACC member and submitted back to an ACC agent. The xlsx file is 
        imported, and a panda series is created
        
        returns: nothing, but updates self.original_pd   
        '''
        self.original_fileName = fileName
        self.original_pd = pd.read_excel(fileName)
        
    def addOriginal_selfVariables(self):
        '''this function pulls a bunch of column-wise data from the member forms and 
        stores them to their corresponding self.variable so they can be referenced later.'''
        df = self.original_pd
        self.original_pd = df.fillna('')
        self.original_pd = df.applymap(str)
        
        # categories expected from the member form:
        self.phone = self.original_pd['Phone number']
        self.address = self.original_pd['Address (please inlcude city and province)']
        self.postal = self.original_pd['Postal Code']
        self.country = self.original_pd['Country']
        self.email = self.original_pd['Email']

        # Title Text
        self.f_name = self.original_pd['First Name'].str.title()
        self.l_name = self.original_pd['Last Name'].str.title()
        
        # concatenate these variables together. This preps data for AddressComplete
        address = self.squishAddress(self.address, self.postal, self.country)
        self.address_series = address
    
    def display_address_series(self):
        ''' AddressComplete returns back a lot of key-value pairs. This function displays
        two columns that are important.

        returns: nothing, but displays two specified columns'''
        
        # what about if just a single series is present? Will it throw an error?
        df = copy.deepcopy(self.address_series)
        df = df[['Line1', 'PostalCode']]
        display(df)
        
    def start(self, template, original):
        '''
        takes in: 2 strings, that are known fileNames. 
        
        start() does the following:
            1. loads the template file/pd and loads the member file/pd
            2. displays the member xlxs file 
                -  if manual editing is needed, pause the process 
                and allow for xcel editing
                - when manual editing is done, reload the new results
                and resume process
            3. every address submitted by an ACC member will be sent to
            AddressComplete to verify and format the data to IMIS specification'''

        while True:                                     # while loops handle user input conditionals and errors
            self.importTemplate(template)
            self.importOriginal(original)
            self.addOriginal_selfVariables()
                                                        
            yes = False
            Quit = False
            reload = False
            
            while not yes:
                df = ACC_stylize.originalStylize(self.original_pd)
                
                display(df)
                print('')
                print('"yes" to proceed, "open" to edit this file in excel, "quit" to end everything')
                answer = input()
                
                if answer == 'yes':
                    yes = True
                elif answer == 'open':
                    while True:
                        answer = input('prompt when "back"')
                        if answer == 'back':
                                                        # reload file because it has just been edited
                            reload = True
                            break
                        elif answer == 'quit':
                            Quit = True
                            break
                        else:
                            print('weird entry:', answer)
                elif answer == 'quit':
                    Quit = True
                else:
                    clear_output()
                    print('your input is not valid:', answer)
                    continue
                                                        # maintain a de-cluttered screen:
                clear_output()
                
                                                        # deals with the closing of the while loops
                if yes == True or Quit == True or reload == True:
                    break
               
            if yes == True or Quit == True:
                break
            if reload == True:
                continue
        
        return Quit 
 
    def squishAddress(self, address, postal, country):
                                                        # concatonate the address columns together
        address = address + ' ' + postal + ' ' + country
                                                        # if duplicates exists, elimintate.
        ### this code does not elmininate duplicate numbers 
        return address.str.replace(r'\b(\w+)(\s+\1)+\b', r'\1')
    
    def convertAddresses(self):
        ''' takes in: a panda SERIES 
        
        Each index in the series will represent an address, which will be in string form. 
        This string will be sent off to AddressComplete where it will return a dictionary 
        containing similar key-value pairs:
            - {'PostalCode':'T1W 0A2, 'CountryName': 'Canada'...etc}
            
        While maintaining the proper index, every string will be converted and all rows will 
        be appended together, forming a dataframe in a configutration sensitive to IMIS formatting .
            
        returns: a dataframe, indexed accordingly'''
                                                        # address_series is coming from squishAddress()
        address_series = self.address_series            # and includes every address in string form
        temp = {}
        for key, value in address_series.items():
            print('key:', key, 'value:', value)
                                                        # tasend string value to address checker
            getAddress = ACC_AddressComplete.AddressComplete(self.Key).runTool(value, self.getACC_object())

            if getAddress == True:
                self.quitting = True

            temp[key] = getAddress
                                                        # update init variable
            self.addressPrint[key] = getAddress
                                                        # T is for transpose
        return pd.DataFrame(temp).T
    
    def updateTemplate_pd(self):
        ''' updateTemplate_pd calls convertAddresses(), which sends back the respective Address Coulmns
        in IMIS ready format.

        return: nothing but template_pd is updated with IMIS read values and formatting
        '''
        
        # categories that will be addded to complete IMIS form
        self.template_pd['Phone number'] = self.phone
        self.template_pd['Email'] = self.email

        ### Here will be delt with names ###
        self.template_pd['First Name'] = self.f_name
        self.template_pd['Last Name'] = self.l_name
        
        # this will send all the addresses off to AddressComplete
        df = self.convertAddresses()
        self.convertedAddresses = df
        
        self.template_pd['Address'] = df['Line1']
        self.template_pd['City'] = df['City']
        self.template_pd['Province'] = df['ProvinceCode']
        self.template_pd['Postal Code'] = df['PostalCode']
        self.template_pd['Country'] = df['CountryName']

    def displayAdress_print(self):
        clear_output()
        countAddress = len(self.addressPrint)
        temp = self.addressPrint
        
        temp = pd.DataFrame(temp).T
        temp = ACC_stylize.addressCompleted_Stylize(temp)
        display(temp)



    def convertToCSV(self):
        df = self.template_pd
        print('Name your file and remember to include .csv')
        fileName = input()
        #If you want to export without the index, simply add index=False
        df.to_csv(fileName, index=False)
        #If you getUnicodeEncodeError , simply add encoding='utf-8'
        #df.to_csv('file_name.csv', encoding='utf-8')
        
def wrapper():
    Key = 'XXXX-XXXX-XXXX-XXXX'
    SearchTerm = 'your-search-term'
    template = 'ACC_Perfect_Template.xlsx'
    original = 'ACC_MailOut_Template.xlsx'

    a = correctACCsubmission(Key)
    a.importOriginal(original)
    a.importTemplate(template)

    if a.start(template, original) == True:
        print('You have ended the process, please start from scratch')
    else:
        #This is the form that I want, now update the IMIS template!
        a.updateTemplate_pd()
        if a.quitting == True:
            print('You have ended the process, please start from scratch')
            return
        
        a.displayAdress_print()
        print('All addresses have been processed...')

        text = "Type 'yes' if you are happy with the corrections, or 'quit' to start over"
        if ACC_inputBehaviours.input_boleanReturn(text):
            # display the auto-formatted table
            clear_output()
            df = ACC_stylize.templateStylize(a.template_pd)
            display(df)

            text = "Type 'yes' if you are happy with this Foramatted Table, or 'quit' to start over"
            if ACC_inputBehaviours.inputThree(text):
                a.convertToCSV()
                print('')
                print('CSV conversion complete, file will be in the path directory')
            else:
                print('You have ended the process, please start from scratch')

        else:
            print('You have ended the process, please start from scratch')
        

        
# In[ ]:
# In[ ]:




