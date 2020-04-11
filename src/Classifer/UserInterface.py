import ResolutionSummarizer
import datetime
from datetime import date
from NaiveClassifier import tokenize_doc
from NaiveClassifier import PATH_TO_DATA
import NaiveClassifier

#Custom date Bill summarization interface
def customSum(billType):
    userInput = '-1'
    
    #Loop until valid userInput is entered
    #Allow user to choose from Bill's from 2019 or 2020, user types 1 or 2 other options return invalid message
    while userInput != 'END':
        userInput = input('\n\nType 1 or 2 for the following options:\n 1: Bills & Resolutions uploaded from 2019 \n 2: Bills & Resolutions uploaded from 2020\n')
        
        if(userInput == '1'):
            startYear = '2019'
            endYear = '2019'
            break
        elif(userInput == '2'):
            startYear = '2020'
            endYear = '2020'
            break
        else:
            print('\n- INVALID INPUT -\n  billType option 1 or option 2 ')
    #Loop until valid userInput is entered
    #User enters a start month of Bill's to be summarized, invalid inputs return a message after which they have another chance to enter the month.        
    while userInput != 'END':
        userInput = input('\nEnter the START month for Bill Summaries in format mm [ex. 03 for march]\n')
        
        if((len(userInput) == 2) and (int(userInput[0]) < 2) and (int(userInput[1]) <= 9)):
            startMonth = userInput
            break
        else:
            print(' \n- INVALID INPUT -\n ')
    #Loop until valid userInput is entered
    #User enters a start day of Bill's to be summarized, invalid inputs return a message after which they have another chance to enter the start day.         
    while userInput != 'END':
        userInput = input('\nEnter the START day for Bill Summaries in format dd [ex. 12]')
        
        if((len(userInput) == 2) and (int(userInput[0]) < 4) and (int(userInput[1]) <= 9)):
            startDay = userInput
            break
        else:
            print(' \n- INVALID INPUT -\n ')
    #Loop until valid userInput is entered
    #User enters a end month of Bill's to be summarized, invalid inputs return a message after which they have another chance to enter the month.           
    while userInput != 'END':
        userInput = input('\nEnter the END month for Bill Summaries in format mm [ex. 03 for march]')
        
        if((len(userInput) == 2) and (int(userInput[0]) < 2) and (int(userInput[1]) <= 9)):
            endMonth = userInput
            break
        else:
            print(' \n- INVALID INPUT -\n ')
    #Loop until valid userInput is entered
    #User enters a end day of Bill's to be summarized, invalid inputs return a message after which they have another chance to enter the day.             
    while userInput != 'END':
        userInput = input('\nEnter the END day for Bill Summaries in format dd [ex. 12]')
        
        if((len(userInput) == 2) and (int(userInput[0]) < 4) and (int(userInput[1]) <= 9)):
            endDay = userInput
            break
        else:
            print(' \n- INVALID INPUT -\n ')
    #Loop until valid userInput is entered
    #User enters the total amount of pages to be summarized        
    while userInput != 'END':
        userInput = input('\nEnter the max amount of Bills you want summarized')
        pageSize = userInput

        if userInput != 'END':
            if billType == '1':
                ResolutionSummarizer.houseResolutionSumm(startYear,startMonth,startDay,endYear,endMonth,endDay,pageSize,nb)
            elif billType == '2':
                ResolutionSummarizer.jointResolutionSumm(startYear,startMonth,startDay,endYear,endMonth,endDay,pageSize,nb)
            break       

#Current day summarization interface
def todaySum(billType):
    #today's date in one string
    rawDate = str(date.today()).split("-")
    
    #Seperate the date string by year, month and day
    todayYear = rawDate[0]
    todayMonth = rawDate[1]
    todayDay = rawDate[2]
    
    #summarize house bills if user inputs 1 or joint bills if user inputs 2
    if billType == '1':
        ResolutionSummarizer.houseResolutionSumm(todayYear,todayMonth,todayDay,todayYear,todayMonth,todayDay,'50',nb)
    elif billType == '2':
        ResolutionSummarizer.jointResolutionSumm(todayYear,todayMonth,todayDay,todayYear,todayMonth,todayDay,'50',nb)

#Current week summarization interface
def weekSum(billType):
    #today's date in one string
    rawDate = str(date.today()).split("-")
    
    #Seperate the date string by year, month and day
    todayYear = rawDate[0]
    todayMonth = rawDate[1]
    todayDay = rawDate[2]
    
    #Subtract the current day to get the beginning of the week
    begOfWeek = (datetime.datetime.today().weekday()) - int(todayDay)
    
    #summarize house bills if user inputs 1 or joint bills if user inputs 2 from the beginning of the week to current day
    if billType == '1':
        ResolutionSummarizer.houseResolutionSumm(todayYear,todayMonth,str(begOfWeek),todayYear,todayMonth,todayDay,'50',nb)
    elif billType == '2':
        ResolutionSummarizer.jointResolutionSumm(todayYear,todayMonth,str(begOfWeek),todayYear,todayMonth,todayDay,'50',nb)   

#First user interaction and option set
def firstInput():
    userInput = '-1';
#Loop until valid input is entered, 1 summarizes House Bills, 2 Summarizes Joint Bills
#An invalid input will print a string and allow the user to enter a valid input   
    while True:
        userInput = input('\nTYPE SUMMARY OPTION BELOW:\n1:HOUSE BILLS\n2:JOINT RESOLUTIONS\n')
        
        if((userInput == '1') or (userInput == '2')):
            return str(userInput)
        elif(userInput == 'END'):
            input('\nExiting program...press enter to continue\n')
            print('\nbye..\n')
            quit()
        else:
            print(' \n- INVALID INPUT -\n ')

#Second user interaction and option set 
def secondInput(billType):
    userInput = 0;
    
#Input of 1 summarizes current day Bill's, input of 2 summarizes current week from day Bill's, input of 3 takes user to a new custom summary option set.
    while True:
        userInput = input('\nTYPE OPTION BELOW:\n1: Summarize todays uploaded Bills\n2: Summarize this weeks uploaded Bills\n3: Summarize custom date uploaded Bills\n')
        if(userInput == '1'):
            todaySum(billType)
            break
        elif(userInput == '2'):
            weekSum(billType)
            break
        elif(userInput == '3'):
            customSum(billType)
            break
        elif(userInput == 'END'):
            input('\nExiting program...press enter to continue\n')
            print('\nbye..\n')
            quit()
        else:
            print(' \n- INVALID INPUT -\n ')
            
#A welcome message at start up
print('Welcome to the Government Bill Summarizer!...')

#Loop options until the user decides to quit
while True:
    
    print('\n\nType END to end the program at any time\n\n')
    
    nb = NaiveClassifier.NaiveBayes(PATH_TO_DATA, tokenizer=tokenize_doc)
    nb.train_model()
    billType = firstInput()
    secondInput(billType)
    
    
    

        


















           
    
   
    
