import json
import requests

#This module gets information from the government api website.
#This module will convert json information and return it as a dictionary and a document count.

#retuns a dictionary containing a Bill's info. It contains congress, session number, bill number, data issued, and the Bill text.
def getWebSiteText(startYear,startMonth, startDay,endYear,endMonth,endDay,pageSize,docNumber,billType,urlType):
    
    #initializes a new dictionary that will contain the Bill's info
    newDict = {}
    if(urlType == '2'):
        #Government API website which can be modified to return different information.
        url = 'https://api.govinfo.gov/collections/BILLS/'+startYear+'-'+startMonth+'-'+startDay+'T00%3A00%3A10Z/'+endYear+'-'+endMonth+'-'+endDay+'T24%3A18%3A10Z?offset=0&pageSize='+pageSize+'&docClass='+billType+'&api_key=A5IBMbRtjbh9c7EYatrZmJNzFxkVgU8AGmtk8XbH'
    else:
        url = 'https://api.govinfo.gov/published/'+ startYear + '-' + startMonth + '-' + startDay + '/' + endYear + '-' + endMonth + '-' + endDay + '?offset=0&pageSize=' + pageSize + '&collection=BILLS&api_key=A5IBMbRtjbh9c7EYatrZmJNzFxkVgU8AGmtk8XbH'
            
    
    
    #returns a website request
    requestPackage = requests.get(url)

    #json file to get to Bill's text information
    j1 = json.loads(requestPackage.text)
    
    #The text file URL
    fileUrl = j1['packages'][docNumber]['packageLink'] + '?api_key=A5IBMbRtjbh9c7EYatrZmJNzFxkVgU8AGmtk8XbH'
     
    #returns file from URL
    requestFile = requests.get(fileUrl)

    #json file to with Bill's information
    j2 = json.loads(requestFile.text)
    
    #Use J2 json file to access the current looked at Bill in text form.
    finalUrl = j2['download']['txtLink'] + '?api_key=A5IBMbRtjbh9c7EYatrZmJNzFxkVgU8AGmtk8XbH'

    requestFinal = requests.get(finalUrl)
    
    #Store information from the API json file j2 into a dictionary
    newDict['congress'] = j2['congress']
    newDict['session'] = j2['session']
    newDict['billNumber'] = j2['billNumber']
    newDict['date'] = j2['dateIssued']
    newDict['text'] = requestFinal.text
    
    #Not all Bill's have a sponsor. If sponsor exists in json store it in newDict.
    if 'members' in j2:
        newDict['sponsor'] = j2['members'][0]['memberName']
        
        if j2['members'][0]['party'] == 'R':
            newDict['sponsorAff'] = 'Republican'
        if j2['members'][0]['party'] == 'D':
            newDict['sponsorAff'] = 'Democrat'
        
    #Not all Bill's have a title. If title exists in json store it in newDict.    
    if  'shortTitle' in j2:
        newDict['title'] = j2['shortTitle'][0]['title']
    
    return newDict
    
#Function used to determine the number of Bill's within time period
def getWebSiteDocCount(startYear,startMonth, startDay,endYear,endMonth,endDay,pageSize,billType,urlType):
    #Government API URL
    if(urlType == '2'):
        #Government API website which can be modified to return different information.
        url = 'https://api.govinfo.gov/collections/BILLS/'+startYear+'-'+startMonth+'-'+startDay+'T00%3A00%3A10Z/'+endYear+'-'+endMonth+'-'+endDay+'T24%3A18%3A10Z?offset=0&pageSize='+pageSize+'&docClass='+billType+'&api_key=A5IBMbRtjbh9c7EYatrZmJNzFxkVgU8AGmtk8XbH'
    else:
        url = 'https://api.govinfo.gov/published/'+ startYear + '-' + startMonth + '-' + startDay + '/' + endYear + '-' + endMonth + '-' + endDay + '?offset=0&pageSize=' + pageSize + '&collection=BILLS&api_key=A5IBMbRtjbh9c7EYatrZmJNzFxkVgU8AGmtk8XbH'
    
    #Store URL request
    requestPackage = requests.get(url)
    #Store json into J2
    j2 = json.loads(requestPackage.text)
    #Return the count or number of Bill's in passed time period.
    return (j2["count"])

    


    