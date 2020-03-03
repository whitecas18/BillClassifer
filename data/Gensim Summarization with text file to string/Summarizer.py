import gensim
import re
from gensim.summarization.summarizer import summarize
from gensim.summarization.textcleaner import split_sentences

# convert text from file to a string
with open("congress.txt", "r") as myfile:
    text = (str(myfile.readlines()))

# remove number chars
text = re.sub('\d', '', text)
# remove certain special chars
text = text.replace('--', '').replace('  ','').replace('(', '').replace(')','').replace('$','')

# create text file
File_object = open("newFile.txt","w")

# write to text file
File_object.writelines(summarize(text , .05))
print(summarize(text ,.05))
