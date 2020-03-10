import gensim
import re
import pathlib
import xml.etree.cElementTree as ET
import string
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from gensim.summarization.summarizer import summarize
from gensim.summarization.textcleaner import split_sentences
from gensim.summarization import keywords
from collections import Counter

def process_bill_files(dir:pathlib.Path, recursive=False):
    kw_bag = Counter()
    doc_count = 0
    for file in dir.glob("*.xml"):
        # print(str(file.absolute()))
        tree = ET.parse(file)
        body = tree.find("legis-body")
        if body is None:
            body = tree.find("amendment-body")
        if body is None:
            body = tree.find("resolution-body")
        if body is None:
            body = tree.find("engrossed-amendment-body")
        if body is None:
            print(file)
            exit(1)
        tBody = ET.ElementTree(body)
        child = ET.Element
        bodyText = ""
        # try:
        for child in tBody.iter():
            if child.text is not None:
                if child.tag == "text" or child.tag == "header":
                    bodyText += child.text + ' '
        # except:
        #      print("Something went wrong", print(child))
        #      print(file.name)
        #      exit(1)
        cleanText = clean(bodyText)
        # try:
        #     print(summarize(cleanText,ratio=0.1))
        # except:
        #     print("-----------------------\n\n\n\n\n\n\n", cleanText, "\n\n\n\n\n\n\n -----------------------")'
        
        try:
            kw = keywords(cleanText, words=5, lemmatize=True, split=True)
            for word in kw:
                kw_bag[word] += 1
        except:
            print(file, '\n' + cleanText)
        doc_count+=1
    return kw_bag, doc_count

def process_summ_files(dir:pathlib.Path, recursive = False):
    kw_bag = Counter()
    doc_count = 0
    for file in dir.glob("*.xml"):
        print(file)
        # print(str(file.absolute()))
        tree = ET.parse(file)
        body = tree.find("./item/summary/summary-text")
        if body is None:
            print(file)
            exit(1)
        print(body.text)
        tBody = ET.ElementTree(body)
        child = ET.Element
        bodyText = ""
        try:
            kw = keywords(bodyText, words=1, lemmatize=True, split=True)
            for word in kw:
                kw_bag[word] += 1
        except:
            print(file, '\n' + bodyText)        
        doc_count += 1
    return kw_bag, doc_count

def clean(text:str):        
    # # remove number chars
    # text = re.sub('\d', '', text)
    # # remove certain special chars
    # text = text.replace('--', '').replace('  ','').replace('(', '').replace(')','').replace('$','')
    period = str.maketrans('','','.')
    transTable = str.maketrans(',',',',string.punctuation.translate(period) + "-()$" + string.digits)
    transText = text.translate(transTable)
    return transText

cwd = pathlib.Path.cwd()
dir_bills = pathlib.Path("data/test_docs/bills/")
dir_billSumm = pathlib.Path("data/gov_docs/BILLSUM-116-hr/")
print("CWD: ", cwd)
kw_d = process_bill_files(dir_bills)
bow_kw = kw_d[0]
num_docs = kw_d[1]
highestKW = (bow_kw.most_common(25)[15:])
plt.title("15th-25th Most Common Keywords of " + str(num_docs) + " docs")

plt.tight_layout(pad=0.22)
plt.xlabel("Token")
plt.ylabel("# docs token was keyword")
plt.bar([x[0] for x in highestKW],[x[1] for x in highestKW], width=0.3)
plt.show()
# cloudText = ''

# for (word,freq) in highestKW:
#     cloudText += word 
# wordcloud = WordCloud().generate(cloudText)

# plt.pyplot.imshow(wordcloud, interpolation='billinear')
# plt.axis("off")
# plt.show()

# processedSum = process_summ_files(cwd/dir_billSumm)
# bow = processedSum[0]
# doc_count = processedSum[1]
# print("Num summaries: ", doc_count, bow)

# convert text from file to a string
# with open("congress.txt", "r") as myfile:
#     text = (str(myfile.readlines()))

# # remove number chars
# text = re.sub('\d', '', text)
# # remove certain special chars
# text = text.replace('--', '').replace('  ','').replace('(', '').replace(')','').replace('$','')

# # create text file
# File_object = open("newFile.txt","w")

# # write to text file
# #File_object.writelines(summarize(text , .05))
# print(summarize(text ,.05))
