import gensim
from gensim.summarization.summarizer import summarize
import requests
from bs4 import BeautifulSoup



#URL to pull text from
url = 'https://www.govinfo.gov/content/pkg/BILLS-116hjres20ih/html/BILLS-116hjres20ih.htm'
#create a request at url
request = requests.get(url)
#request page
html_page = request.content
#get unparsed content from webpage
contentGetter = BeautifulSoup(html_page, 'html.parser')
#get text from webpage
webpageText = contentGetter.find_all(text=True)
#create list of unwanted words from text
removeWords = ['[document]','noscript','header','html','meta','head', 'input','script','<DOC>','``Article--','<all>']
#initialize string output
output =""
#iterate through webpage text checking for unwanted words
for text in webpageText:
    if text.parent.name not in removeWords:
        output += '{} '.format(text)

#further parse text replacing certain words with a single space.
line = output.replace("\n"," ").replace("  "," ").replace("   "," ").replace("    "," ").replace("     "," ").replace("      "," ").replace("       "," ")

#split text at Joint resolution where the text that needs to be summarized starts
hrs = line.split("JOINT RESOLUTION")

# print summarization to console, always summarize from index 1.
print(summarize(hrs[1], .45))