from easygui import *
import numpy as np 
import json

class Interface(object):
    def __init__(self, database):
        self._database = database #database.asdict()

    def _getQueryFromUser(self):
        msg = "Search for movies"
        title = "Search Engine Application"
        fieldNames = ["Title", "Genre", "Director", "Date", "Runtime"]
        fieldValues = multenterbox(msg, title, fieldNames)

        # make sure that none of the fields was left blank
        while 1:
            if fieldValues == None: 
                break
            
            errmsg = ""
            oneFieldProvided = False

            for i in range(len(fieldNames)):
              if fieldValues[i].strip() != "":
                oneFieldProvided = True
                break  

            if oneFieldProvided: 
                break # no problems found
            else:
                errmsg = "At least one field should be provided."
            
            fieldValues = multenterbox(errmsg, title, fieldNames, fieldValues)

        dictList = zip(fieldNames, fieldValues)
        result = dict(dictList)

        return result
        
    def _showRetrievedDocuments(self, retrievedDocuments):
        result = ""
        
        for (document, rank) in retrievedDocuments:
            result = result + str(json.dumps(self._database[document], indent=1)) + "\n\n"
        
        result = result.replace('"', '')
        result = result.replace('{', '')
        result = result.replace('}', '')

        print(result)    

        textbox(str(len(retrievedDocuments)) + " results", "Retrieved Documents", result)

        self._getQueryFromUser()

    def _searcher(self):
        query = myInterface._getQueryFromUser()
        documentsList = retrieveDocuments(query)

        myInterface._showRetrievedDocuments(documentsList)

def retrieveDocuments(query):
    return [(0, 5), (1, 4)]

# Testing
if __name__ == '__main__':

    database = [{'Title': "The Lord of The Rings",
                    'Genre': "Action & Adventure",
                    'Director': "Peter Jackson",
                    'Date': "01/01/2002",
                    'Runtime': "165 minutes",
                    'Website': "IMDB"},

                {'Title': "The Matrix",
                    'Genre': "Science Fiction",
                    'Director': "The Wachowski Brothers",
                    'Date': "31/03/1999",
                    'Runtime': "136 minutes",
                    'Website': "Rotten Tomato"}
                ]

    myInterface = Interface(database)
    myInterface._searcher()
    


