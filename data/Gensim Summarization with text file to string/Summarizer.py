import gensim
import re
import pathlib
import xml.etree.cElementTree as ET
import string
from gensim.summarization.summarizer import summarize
from gensim.summarization.textcleaner import split_sentences
from gensim.summarization import keywords
def read_files(dir:pathlib.Path, recursive=False):

    for file in dir.glob("*.xml"):
        print(str(file.absolute()))
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
        for child in tBody.iter("text"):
            if child.text is not None:
                bodyText += child.text
        # except:
        #      print("Something went wrong", print(child))
        #      print(file.name)
        #      exit(1)
        cleanText = clean(bodyText)
        print(summarize(cleanText,ratio=0.05))
        print(keywords(cleanText, ratio = 0.1))

def clean(text:str):        
    # # remove number chars
    # text = re.sub('\d', '', text)
    # # remove certain special chars
    # text = text.replace('--', '').replace('  ','').replace('(', '').replace(')','').replace('$','')
    transTable = str.maketrans(',',',',string.punctuation + "-()$" + string.digits)
    transText = text.translate(transTable)

cwd = pathlib.Path.cwd()
dir_path = pathlib.Path("data/gov_docs/BILLS-116-1-hr/")
read_files(cwd/dir_path)
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
