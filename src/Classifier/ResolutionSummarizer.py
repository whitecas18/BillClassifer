from gensim.summarization.summarizer import summarize
import WebsiteInfoGetter
import collections
import re
import matplotlib.pyplot as plt 
from gensim.parsing.preprocessing import remove_stopwords
from gensim.parsing.preprocessing import strip_numeric
from gensim.parsing.preprocessing import strip_short
import asciiplotlib as apl
import numpy

#This module summarizers bills of various types and generates an ascii bar graph.

#summarizer parameters are the dates of the documents, first is the start date, second is the end date. Dates are in 4,2,2 format (yyyy,mm,dd,yyyy,mm,dd,).
def jointResolutionSumm(startYear,startMonth,startDay,endYear,endMonth,endDay,pageSize,nb,urlType):
    userChoice = '-1'
    #Dictonary to return Bill Type string, depending on wait Naive classifier returns.
    billTypeDict = {'fire':'Firearm/Explosive Bill', 'gov':'Government/Political Bill', 'enviro':'Environmental\Weather Bill','health':'Healthcare\Medicine\Welfare Bill'}
    
    #Number of bills returned from WebsiteInfoGetter    
    numDocs = WebsiteInfoGetter.getWebSiteDocCount(startYear,startMonth,startDay,endYear,endMonth,endDay,pageSize,'hjres',urlType)
    
    #Print string of how many documents are available to summarize from given date.
    print("\nThere were " + str(numDocs) + " joint resolutions uploaded from " + str(startMonth) + "-" + str(startDay) + "-" + str(startYear) + " to " + str(endMonth) + "-" + str(endDay) + "-" + str(endYear)+"\n")
    
    #If numDocs is larger than requested size then use numDocs instead.
    if(int(numDocs) < int(pageSize)):
        numSum = numDocs
    else:
        numSum = pageSize
    
    #Get text and summarize for the given amount of documents     
    for docNumber in range(0 , (int(numSum) - 1)):
        
        if userChoice == '0':   
            userChoice = input('\nPress ENTER to summarize next Bill or type END to end summarizations\n')
            print('\nPlease wait. \nProcessing', end ='')
            if userChoice == 'END':
                break
            else:
                userChoice = '1'

        
        #Dictionary containing Bill information from json file
        newDict = WebsiteInfoGetter.getWebSiteText(startYear,startMonth,startDay,endYear,endMonth,endDay,pageSize,docNumber,'hjres',urlType)
        billDate = newDict['date'].split("-")
        print('.', end ='')
        #if(dateChecker(startYear,startMonth,startDay,endYear,endMonth,endDay,pageSize,billDate) == False):
        #    continue
        
        #remove list of unwanted words from text 
        removeWords = ['[document]','noscript','header','html','meta','head', 'input','script','<DOC>','``Article--','<all>',"\n"]
        #remove list of spacing
        removeSpaces = ["  ","   ","   ","    ","      "]
        
        #Set text to the Bill text to be summarized from dictionary
        text = newDict["text"]
        print('.', end ='')
        #if a word matches a word in removeWords, remove the word.
        for word in removeWords:
            text.replace(word, "")
        
        #replace excessive spaces with a single space    
        for space in removeSpaces:
            text.replace(space, " ")
        print('.', end ='')
        #split text at Joint resolution where the text that needs to be summarized starts
        splitText = text.split("JOINT RESOLUTION")
        
        #Set bow to tokenized words from text
        bow = nb.tokenize_doc(text)
        #Classify a Bill's text using NaiveClassifier's classify function and set this to billType.
        billType = nb.classify(bow, .2)
        print('.\n')
        #Print the information for current Bill being looked at.
        #If certain information is unavailable, it is not printed.
        if(('title' in newDict) and ('sponsor' in newDict)):
            print("Formal Title: " + newDict['title'] + "\n" + newDict['congress'] + "th Congress" + "\nSession: " + newDict['session'] + "\nResolution: " + newDict['billNumber'])
            print('Date Issued: ' + newDict['date'] + "\nBill Sponsor and Pol. Party: " + newDict['sponsor'] + " " + newDict['sponsorAff'])
            print('Bill type based on classifier: ' + billTypeDict[billType])
        elif( ('title' in newDict) and ('sponsor' not in newDict)):
            print("Formal Title: " + newDict['title'] + "\n" + newDict['congress'] + "th Congress" + "\nSession: " + newDict['session'] + "\nResolution: " + newDict['billNumber'])
            print('Date Issued: ' + newDict['date'] + "\nNo Sponsor")
            print('Bill type based on classifier: ' + billTypeDict[billType])
        elif(('sponsor' in newDict) and ('title' not in newDict)):
            print('No Formal Title' + "\n" + newDict['congress'] + "th Congress" + "\nSession: " + newDict['session'] + "\nResolution: " + newDict['billNumber'])
            print('Date Issued: ' + newDict['date'] + '\nNo Sponsor')
            print('Bill type based on classifier: ' + billTypeDict[billType])
        else:       
            print('No Formal Title\n ' + newDict['congress'] + "th Congress" + "\nSession: " + newDict['session'] + "\nResolution: " + newDict['billNumber'])
            print('Date Issued: ' + newDict['date'] + newDict['date'] + '\nNo Sponsor')
            print('Bill type based on classifier: ' + billTypeDict[billType])
            
        topText = topWords(text,5)
        createPlot(topText,5)
        # print summarization to console, always summarize from index 1.
        #Check where the Bill was split based on length of list
        #Summarize and print current Bill text
        
        print("\n[BILL SUMMARY]")
        if 1 < len(splitText):
            print("\n" + (summarize(splitText[1], .75)) + "\n")
        else:
            print("\n" + (summarize(splitText[0], .75)) + "\n")
        
        
        userChoice = '0'
        
    userChoice = input('\nAll Bills have been summarized, press ENTER to return to main screen, type END to close program.')
    if userChoice == 'END':
        input('\nExiting program...press enter to continue\n')
        quit()       

#Function summarizes house bill  
def houseResolutionSumm(startYear,startMonth,startDay,endYear,endMonth,endDay,pageSize,nb,urlType):
    userChoice = '-1'
    #Dictonary to return Bill Type string, depending on wait Naive classifier returns.
    billTypeDict = {'fire':'Firearm/Explosive Bill', 'gov':'Government/Political Bill', 'enviro':'Environmental\Weather Bill','health':'Healthcare\Medicine\Welfare Bill'}    
   
    #Number of bills returned from WebsiteInfoGetter    
    numDocs = WebsiteInfoGetter.getWebSiteDocCount(startYear,startMonth,startDay,endYear,endMonth,endDay,pageSize,'hr',urlType)
    
    #Print string of how many documents are available to summarize from given date.
    print("\nThere were " + str(numDocs) + " house resolutions uploaded from " + str(startMonth) + "-" + str(startDay) + "-" + str(startYear) + " to " + str(endMonth) + "-" + str(endDay) + "-" + str(endYear)+"\n")
    
    #If numDocs is larger than requested size then use numDocs instead.
    if(int(numDocs) < int(pageSize)):
        numSum = numDocs
    else:
        numSum = pageSize
    
    #Get text and summarize for the given amount of documents     
    for docNumber in range(0 , (int(numSum) - 1)):
    
    
        if userChoice == '0':   
            userChoice = input('\nPress ENTER to summarize next Bill or type END to end summarizations\n')
            print('\nPlease wait. \nProcessing', end ='')
            if userChoice == 'END':
                break
            else:
                userChoice = '1'
    
    
        
        newDict = WebsiteInfoGetter.getWebSiteText(startYear,startMonth,startDay,endYear,endMonth,endDay,pageSize,docNumber,'hr',urlType)
        billDate = newDict['date'].split("-")
        print('.', end ='')
        #if(dateChecker(startYear,startMonth,startDay,endYear,endMonth,endDay,pageSize,billDate) == False):
        #    continue
         
        #remove list of unwanted words from text 
        removeWords = ['[document]','noscript','header','html','meta','head', 'input','script','<DOC>','``Article--','<all>',"\n"]
        #remove list of spacing
        removeSpaces = ["  ","   ","   ","    ","      "]
        
        text = newDict["text"]
        print('.', end ='')
       
        #if a word matches a word in removeWords, remove the word.
        for word in removeWords:
            text.replace(word, "")
        
        #replace excessive spaces with a single space    
        for space in removeSpaces:
            text.replace(space, " ")
        print('.', end ='')
        #split text at Joint resolution where the text that needs to be summarized starts
        splitText = text.split("IN THE HOUSE OF REPRESENTATIVES")
        
        #Set bow to tokenized words from text
        bow = nb.tokenize_doc(text)
        #Classify a Bill's text using NaiveClassifier's classify function and set this to billType.
        billType = nb.classify(bow, .2)
        print('.\n')
        #Print the information for current Bill being looked at.
        #If certain information is unavailable, it is not printed.    
        if(('title' in newDict) and ('sponsor' in newDict)):
            print("Formal Title: " + newDict['title'] + "\n" + newDict['congress'] + "th Congress" + "\nSession: " + newDict['session'] + "\nResolution: " + newDict['billNumber'])
            print('Date Issued: ' + newDict['date'] + "\nBill Sponsor and Pol. Party: " + newDict['sponsor'] + " " + newDict['sponsorAff'])
            print('Bill type based on classifier: ' + billTypeDict[billType])
        elif( ('title' in newDict) and ('sponsor' not in newDict)):
            print("Formal Title: " + newDict['title'] + "\n" + newDict['congress'] + "th Congress" + "\nSession: " + newDict['session'] + "\nResolution: " + newDict['billNumber'])
            print('Date Issued: ' + newDict['date'] + "\nNo Sponsor")
            print('Bill type based on classifier: ' + billTypeDict[billType])
        elif(('sponsor' in newDict) and ('title' not in newDict)):
            print('No Formal Title' + "\n" + newDict['congress'] + "th Congress" + "\nSession: " + newDict['session'] + "\nResolution: " + newDict['billNumber'])
            print('Date Issued: ' + newDict['date'] + '\nNo Sponsor')
            print('Bill type based on classifier: ' + billTypeDict[billType])
        else:       
            print('No Formal Title\n ' + newDict['congress'] + "th Congress" + "\nSession: " + newDict['session'] + "\nResolution: " + newDict['billNumber'])
            print('Date Issued: ' + newDict['date'] + newDict['date'] + '\nNo Sponsor')
            print('Bill type based on classifier: ' + billTypeDict[billType])
        
        
        topText = topWords(text,5)
        createPlot(topText,5)
        
        
        print("\n[BILL SUMMARY]")
        #Check the length of the Bill and choose the correct summary to word ratio depending on length
        if 1 < len(splitText):
            if len(splitText[1]) > 30:
                if len(splitText[1]) > 60:
                    print("\n" + (summarize(splitText[1], .20)) + "\n")
                else:
                    print("\n" + (summarize(splitText[1], .25)) + "\n")
            else:
                print("\n" + (summarize(splitText[1], .70)) + "\n")
        else:
            if len(splitText[0]) > 30:
                if len(splitText[0]) > 60:
                    print("\n" + (summarize(splitText[0], .20)) + "\n")
                else:
                    print("\n" + (summarize(splitText[0], .25)) + "\n")
            else:
                print("\n" + (summarize(splitText[0], .70)) + "\n")
        
        userChoice = '0'

    userChoice = input('\nAll Bills have been summarized, press ENTER to return to main screen, type END to close program.')
    if userChoice == 'END':
        input('\nExiting program...press enter to continue\n')
        quit()       

#Finds the top words in a bill
def topWords(billText, numberWords):
    
    text = remove_stopwords(billText)
    text = strip_numeric(text)
    text = strip_short(text,minsize=2)
    words = re.findall(r'\w+', text)
    topW = collections.Counter(words).most_common(numberWords)
    
    return topW

#Creates an ascii bar graph plot
def createPlot(topW, numberWords):
       
    labels = []
    numbers = []
    for l,n in topW:
        labels.append(l)
        numbers.append(n)
    
    print('\n[TOP ' + str(numberWords) + ' WORDS IN BILL]\n')    
    fig = apl.figure()
    fig.barh(numbers,labels,force_ascii=True)
    fig.show()
        
#Creates and generates matplotlib plot    
def createMatPlot(topW, numberWords):   
    plt.xticks(range(len(numbers)), labels)
    plt.xlabel('WORDS')
    plt.ylabel('WORD COUNTS')
    plt.title('TOP ' + str(numberWords) + ' WORDS IN BILL')
    plt.bar(range(len(numbers)), numbers) 
    plt.show()

#Function can be uncommented to check if bill dates fall in the correct range.
'''
#Function to check if a date falls within the correct start and end date
def dateChecker(startYear,startMonth,startDay,endYear,endMonth,endDay,pageSize,billDate):
    
        if((billDate[0] < startYear) or (billDate[0] > endYear)):
            return False
        
        elif(billDate[0] == startYear):
            if((billDate[1] < startMonth) or (billDate[1] == startMonth and billDate[2] < startDay)):
                return False
            
        elif(billDate[0] == endYear):
            if((billDate[1] > endMonth) or (billDate[1] == endMonth and billDate[2] > endDay)):
                return False
        
        return True
'''    
