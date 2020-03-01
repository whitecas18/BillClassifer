import gensim
from gensim.summarization.summarizer import summarize
from gensim.summarization.textcleaner import split_sentences


with open("congress.txt", "r") as myfile:
    text = str(myfile.readlines())
    

print(summarize((text), .1))
