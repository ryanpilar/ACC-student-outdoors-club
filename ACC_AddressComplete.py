#!/usr/bin/env python
# coding: utf-8

# In[1]:


import copy
import urllib
import ACC_Main
import xml.dom.minidom

class AddressComplete():
    '''
    class AddressComplete is a collection of functions that handle the input, and return, of an address
    (a string) and its submission to the Canada Post API.

    In addition, functions dealing with the selection and input behaviours help navigate the
    Canada Post suggestions that exist '''
    
    def __init__(self, Key):
        self.returnedResults = None
        
        self.Key = Key
        self.SearchTerm = None
        
        self.df_list = []
        self.decision_list = []
        
        self.returnBack = []
        self.returnBack_clean = None
        self.ACC_object = None
        
    def getAddressComplete_object(self):
        return self
    
    def AddressComplete_Interactive_Retrieve_v2_11(self, Key, Id):
        '''
        takes in: a ['Key'] and a referance ['Id']

        before this 'Interactive_Retrieve' function can be called, AddressComplete_Interactive_Find_v2_10
        needs to be called first. 'Interactive_Find' returns a referance 'Id'. This referance 'Id' is plugged
        into 'Interactive_Retrieve' to retrieve the address details of said address

        returns: a dictionary
        '''
                                                        #Build the url
        requestUrl = "http://ws1.postescanada-canadapost.ca/AddressComplete/Interactive/Retrieve/v2.11/xmla.ws?"
        requestUrl += "&" +  urllib.parse.urlencode({"Key":Key})
        requestUrl += "&" +  urllib.parse.urlencode({"Id":Id})

                                                        #Get the data
        dataDoc = xml.dom.minidom.parseString(urllib.request.urlopen(requestUrl).read())

                                                        #Get references to the schema and data
        schemaNodes = dataDoc.getElementsByTagName("Column")
        dataNotes = dataDoc.getElementsByTagName("Row")

        #Check for an error
    #     if len(schemaNodes) == 4 and schemaNodes[0].attributes["Name"].value == "Error":
    #         raise Exception, dataNotes[0].attributes["Description"].value

                                                        #Work though the items in the response
        results = []
        for dataNode in dataNotes:
            rowData = dict()
            for schemaNode in schemaNodes:
                key = schemaNode.attributes["Name"].value
                value = dataNode.attributes[key].value
                rowData[key] = value
            results.append(rowData)

        return results

      #FYI: The output is an array of key value pairs, the keys being:
                                                      #Id
                                                      #DomesticId
                                                      #Language
                                                      #LanguageAlternatives
                                                      #Department
                                                      #Company
                                                      #SubBuilding
                                                      #BuildingNumber
                                                      #BuildingName
                                                      #SecondaryStreet
                                                      #Street
                                                      #Block
                                                      #Neighbourhood
                                                      #District
                                                      #City
                                                      #Line1
                                                      #Line2
                                                      #Line3
                                                      #Line4
                                                      #Line5
                                                      #AdminAreaName
                                                      #AdminAreaCode
                                                      #Province
                                                      #ProvinceName
                                                      #ProvinceCode
                                                      #PostalCode
                                                      #CountryName
                                                      #CountryIso2
                                                      #CountryIso3
                                                      #CountryIsoNumber
                                                      #SortingNumber1
                                                      #SortingNumber2
                                                      #Barcode
                                                      #POBoxNumber
                                                      #Label
                                                      #Type
                                                      #DataLevel

    def AddressComplete_Interactive_Find_v2_10(self, Key, SearchTerm, LastId, SearchFor, Country, LanguagePreference, MaxSuggestions, MaxResults):
        '''
        this function interacts with the Canada Post API. Give this function an address in
        string format, and it will return a list of suggestions.

        takes in 8 paramaster:
            1 - key, string
            2 - searchTerm, the text that you want searched
            3 - LastId, use this when you have a container of addresses that you need unpacked
            4 - Country, CAD is default
            5 - Language, english is default
            6 - MaxSuggestions
            7 - MaxResults   

        returns: a dictionary of dictionaries '''
                                                        # Build the url
        requestUrl = "http://ws1.postescanada-canadapost.ca/AddressComplete/Interactive/Find/v2.10/xmla.ws?"
        requestUrl += "&" +  urllib.parse.urlencode({"Key":Key})
        requestUrl += "&" +  urllib.parse.urlencode({"SearchTerm":SearchTerm})
        requestUrl += "&" +  urllib.parse.urlencode({"LastId":LastId})
        requestUrl += "&" +  urllib.parse.urlencode({"SearchFor":SearchFor})
        requestUrl += "&" +  urllib.parse.urlencode({"Country":Country})
        requestUrl += "&" +  urllib.parse.urlencode({"LanguagePreference":LanguagePreference})
        requestUrl += "&" +  urllib.parse.urlencode({"MaxSuggestions":MaxSuggestions})
        requestUrl += "&" +  urllib.parse.urlencode({"MaxResults":MaxResults})

                                                        #Get the data
        dataDoc = xml.dom.minidom.parseString(urllib.request.urlopen(requestUrl).read())

                                                        #Get references to the schema and data
        schemaNodes = dataDoc.getElementsByTagName("Column")
        dataNotes = dataDoc.getElementsByTagName("Row")

                                                        #Check for an error
    #     if len(schemaNodes) == 4 and schemaNodes[0].attributes["Name"].value == "Error":
    #         raise Exception #, dataNotes[0].attributes["Description"].value

                                                        #Work though the items in the response
        results = []
        for dataNode in dataNotes:
            rowData = dict()
            for schemaNode in schemaNodes:
                key = schemaNode.attributes["Name"].value
                value = dataNode.attributes[key].value
                rowData[key] = value
            results.append(rowData)

        self.returnedResults = results
                                                        # make a dataframe with the above results
        self.df_list.append(ACC_Main.pd.DataFrame(self.returnedResults))
        
                                                        #FYI: The output is an array of key value pairs, the keys being:
                                                        #Id
                                                        #Text
                                                        #Highlight
                                                        #Cursor
                                                        #Description
                                                        #Next
    def mainSearch(self, LastId = ''):

        ''' is a wrapper function that hard codes a bunch of paramaters that are needed
        to do the initial call to the Canada Post API

        takes in:
            Key - string, the key you need to access your API account
            SearchTerm - string, text search entry

        returns: nothing, but self.returnedResults is updated, via AddressComplete_Interactive_Find_v2_10() 
        '''
        SearchFor = 'Everything'
        Country = 'CAN'
        LanguagePreference = 'en'
        MaxSuggestions = 15
        MaxResults = 100
                                                        # creates a list of df frames, each element being a suggestion
        self.AddressComplete_Interactive_Find_v2_10(self.Key, self.SearchTerm, LastId, SearchFor, Country, LanguagePreference, MaxSuggestions, MaxResults)

    def goBack(self):
        '''this function removes the last item in df_list'''
        try:
            self.df_list.pop()
        except IndexError:
            print('')
            print('You have pressed "back" too many times')

    def find_or_retrieve(self, df, row_indexer):
        
        column_indexer = 'Next'
        Next = df.loc[row_indexer,column_indexer]
        column_indexer = 'Id'
        Id = df.loc[row_indexer,column_indexer]
        
        if Next == 'Find':
            # 'Find' signifies a container holding mutiple suggestions
            ### send LastId back into AddressComplete to parse addresses in the container
            self.mainSearch(LastId = Id)
            # reload output so the last step is reflected. 
            ### and prompt user for a selection decision 
            self.selectCell()
            
        elif Next == 'Retrieve':
            # send Id to a new Canada Post method.... RetrieveID
            results = self.AddressComplete_Interactive_Retrieve_v2_11(self.Key, Id)
            self.returnBack = results
        else:
            print('WTF?, should only be "Find" or "Retrieve:"', Next)

    def modifySubmission(self):
        
        keys = {'City':[], 'Line1':[], 'ProvinceCode':[], 'PostalCode':[], 'CountryName':[]}
        aDict = {}
        # make this a dataframe so it can be stylized
        df = ACC_Main.pd.DataFrame(keys).T


        for key in keys:

            ACC_Main.clear_output()
            
            # send df to stylesheet thang
            display(ACC_Main.ACC_stylize.addressModify_Stylize(df))
            print('Member submission to be updated:', "\033[1m" + self.SearchTerm + "\033[0m", '\n')

            print('Manually update:', key)
            text = input()
            df[key] = text
            aDict[key] = text

        # give the user one last chance to make a final adjustment
        question = "Are you happy with your changes? 'yes', 'no', 'quit'"
        
        while True:
            print(question)
            text = input()
            
            if text == 'no':
                return self.modifySubmission()

            elif text == 'yes':
                return aDict

            elif text == 'quit':
                return text
            else:
                print('Invalid entry, try again...')


    def inputBehaviour(self):

        # if there is only one item in pd_list, don't allow 'back'
        if len(self.df_list) > 1:
            # remember to pass the object
            return ACC_Main.ACC_inputBehaviours.input_reg(self.getAddressComplete_object())
        else:
            return ACC_Main.ACC_inputBehaviours.input_restrict(self.getAddressComplete_object())

                
    def selectCell(self):
                                                            # clear the output
        ACC_Main.clear_output()

        if self.df_list == []:
            print('There is nothing to display, please start over')
                                                            
        else:
            # this is going to display all the completed addresses
            self.display_df_list()                          
            print('Original Submission:', "\033[1m" + self.SearchTerm + "\033[0m")

            # will be a int, aDict, 'quit' or 'back'
            row_indexer = self.inputBehaviour()             # initiate input box behaviour
                                                            
            if type(row_indexer) == int:                    
                column_indexer = 'Id'
                                                            # row selection on the last element, [-1]
                df = self.df_list[-1]
                # is the selected row find or retrieve?
                ## and collect the results, whether its the original string or a CanadaPost object
                                                            # use the row_indexer to choose column

                try:
                    self.find_or_retrieve(df, row_indexer)
                except:

                    print('You have chosen an index that is out of range. Type "yes" to choose again.')
                    hold = input()
                    self.selectCell()
                
            elif type(row_indexer) == dict:
                self.returnBack = row_indexer
                
            elif row_indexer == 'quit':
                self.ACC_object.quitting = True            


    def display_df_list(self):
        countAddress = len(self.ACC_object.addressPrint)
        temp = self.ACC_object.addressPrint
        
        temp = ACC_Main.pd.DataFrame(temp).T
        temp = ACC_Main.ACC_stylize.addressCompleted_Stylize(temp)
        display(temp)
        
        aList = copy.deepcopy(self.df_list)

        # this is suppose to be grabbing 'text', 'description' but they may not be there for manual entries
        for i in range(len(aList)):
            df = aList[i]
            df = df[['Text', 'Description']]
            df = ACC_Main.ACC_stylize.addressChecker_Stylize(df)

            #df = self.ACC_Main.ACC_stylize.addressStylize(df)
            
            display(df)


    def returnBack_(self):
        ''' AddressComplete-Retrieve returns a lengthy dictionary,
        with many keys that are not useful to this project. This program
        first grabs the english version, and from that, grabs 5 keys:
            - City, Line1, ProvinceCode, PostelCode, CountryName
        
        returns a dictionary containing the above keys
        '''   
        
        # grab the english version and leave the French behind:
        aDict_list = copy.deepcopy(self.returnBack)
        
        if type(aDict_list) == dict:
            # this should be the manual entry
            return aDict_list

        else:
            # this should be from AddressComplete (aList)
            for aDict in aDict_list:
                
                if aDict['Language'] == 'ENG':
                    results = aDict
                    self.returnBack = results

        # get only the headers you want:
        temp = {}
        aDict = copy.deepcopy(self.returnBack)

        for key, value in aDict.items():
                    
            if key in {'City', 'Line1', 'ProvinceCode', 'PostalCode', 'CountryName'}:
                temp[key] = value

        return temp
      
    def runTool(self, SearchTerm, ACC_object):
        # grab suggestions, append df and display df_list
        # ask what index you would like to proceed with
        # make new df and add it to df_list, 
        # display df_list and ask what index again
        
        
        # save the SearchTerm so you can referance it later
        self.SearchTerm = SearchTerm
        self.ACC_object = ACC_object
        
                                                        # this will create the first list element in self.df_list
        self.mainSearch(LastId = '')
        
        self.selectCell()

        if self.ACC_object.quitting == False:
            z = self.returnBack_()
            self.returnBack_clean = z
            print('returnBack_clean official', self.returnBack_clean)
            
            return self.returnBack_clean

        else:
            return True

def convertAddresses(self, address_series):
    ''' takes in: a panda series 
    
    Each index in the series will represent an address, which will be in string form. 
    This string will be sent off to AddressComplete where it will return a dictionary 
    containing the address broken down into its components:
        - {'PostalCode':'T1W 0A2, 'CountryName': 'Canada'... etc.}
    maintaining the proper index, every string will be converted, and all rows will 
    be appended together forming a dataframe.
        
    '''
    temp = {}
    for key, value in address_series.items():
        print('key:', key, 'value:', value)
        # take the value and send it to address checker
        temp[key] = ACC_AddressComplete.AddressComplete().runTool(SearchTerm = value)
        
    print(temp)


# In[ ]:




