# AUTHOR: 		Dillon Roberts
# EMAIL: 			robertsd13@students.ecu.edu
# FILE: 			tokenizer.py
# TAB SPACES:	2
# CLA:				DATA_PATH PATH_STOPWORDS
# PY-VERS:		Python 3.7.6 32-bit [ran on Windows 10 64-bit]
# DESCRIPTION:
# 			This file uses given directory path and file path to
# 			tokenize words of the files in the directory into the d_model object.
# 			It contains definitions for maintaining counts of words within basic files
# 			containing text. Given no flags, it will tokenize, stem words to their
# 			basic form, and remove stopwords based off a stopword file and store their
# 			frequencies within its model variables.
# 			Files should be readable with UTF-8.
#import codecs
#import os
import cProfile
import io
import pstats
from pstats import SortKey
import glob
import sys
import string
try:
	import nltk
	from nltk.corpus import stopwords
except:
	print("Failed to find NLTK. Make sure the Python version you called the script with is compatible with it.")
	print("If you are not running 32-bit Python it also may not import correctly")
	print("Your version: ", sys.version_info)
	print("Terminating")
	exit(1)
import textwrap
import pathlib
from collections import Counter, defaultdict

class d_model:
	def __init__(self, d_path, out_path=None, path_stopwords=None):
		# d_path: 				path to data
		# path_stopwords:	Path to a text file of stopwords
		self.data_path = d_path
		self.path_stopwords = path_stopwords
		self.stopwords = set()
		if path_stopwords is None:
			self.stopwords = set(stopwords.words('english'))
		self.out_path = out_path

		self.vocab = set()
		self.total_word_counts = 0
		self.word_counts = Counter()

	def load_stopwords(self):
		if self.path_stopwords is None:
			return None
		# Load the stopword file and store its contents
		f_words = open(self.path_stopwords, 'r')
		words = f_words.read()
		split_words = words.split()
		for word in split_words:
			self.stopwords.add(word)
		f_words.close()
	
	def process(self, only_tokenize=False):
		# Populate the word counts from the a given file path in
		# self.data_path. Perform stemming and stopword removal
		# unless only_tokenize is true

		self.load_stopwords()
		# TODO Change this to work with any OS path (win/mac/unix)
		files = [f for f in glob.glob(self.data_path + "\\*")]
		for file in files:
			file = open(file, 'r')
			self.tokenize_doc(file.read(), only_tokenize)
			file.close()		
		self.update_model()
		self.stem()
		self.remove_sw()
		self.update_model()

	def stem(self, minChars = 3):
		# Stem all the words in the vocabulary.
		# Removes the original word from the word counts
		# and adds it to the count of the stemmed word.
		ps = nltk.PorterStemmer()
		for word in list(self.vocab):
			self.vocab.remove(word)
			if len(word) < minChars:		
				self.total_word_counts -= self.word_counts.pop(word, None)
			else:
				stemmed = ps.stem(word)
				count = self.word_counts.pop(word, None) 
				self.word_counts[stemmed] += count # This seems mundane, but necessary to prevent double counting
				self.vocab.add(stemmed)

		self.update_model()
		
	def remove_sw(self):
		stopwords = self.stopwords
		for stopword in stopwords:
			self.total_word_counts -= self.word_counts.pop(stopword, 0.0)
		self.vocab.difference_update(stopwords)

	def tokenize_doc(self, doc, only_tokenize=False):
		# Given a doc and a flag to only tokenize
		# process the tokens of the doc
		tokens = doc.split()
		
		# Replace uppercase with lowercase and remove all punctuation + digits
		symbols = '‘-'
		replace_table = str.maketrans(string.ascii_uppercase,string.ascii_lowercase, symbols + string.punctuation + string.digits)
		for token in tokens:
			self.word_counts[token.translate(replace_table)]+=1.0
		# Some strings become empty, it's faster to not check and delete them at the end
		self.word_counts.pop("", 0.0)
	
	def sliceCorpusEnds(self, percentage=0.10):
		# Remove the top and bottom percentage of words
		# in the corpus and return.
		margin_words = self.word_counts.most_common()
		percentage_sum = 0.0
		sum_tokens = 0.0
		removed_tokens = 0.0
		remove_words = set() # Remember these for managing vocabulary
		for wordV in margin_words: # Highest frequency tokens
			remove_words.add(wordV[0])
			word_counts = self.word_counts.pop(wordV[0])
			sum_tokens += word_counts
			percentage_sum = (sum_tokens / self.total_word_counts)
			if percentage_sum>=percentage:
				removed_tokens += sum_tokens
				break
		percentage_sum = 0.0
		sum_tokens = 0.0
		while percentage_sum <= percentage: # Lowest frequency tokens
			wordV = margin_words.pop()
			remove_words.add(wordV[0])
			word_counts = self.word_counts.pop(wordV[0])
			sum_tokens += word_counts
			percentage_sum = (sum_tokens / self.total_word_counts)
		removed_tokens += sum_tokens
		self.total_word_counts -= removed_tokens
		self.vocab.difference_update(remove_words)

	def update_model(self):
		self.vocab = set()
		self.total_word_counts = 0

		self.vocab.update(self.word_counts.keys())
		self.total_word_counts += sum(self.word_counts.values())

	def report(self, show_word_lists=False):
		print ("-------Corpus Stats-------")

		print ("Token Count: ", self.total_word_counts)
		print ("Vocabulary Size: ", len(self.vocab))
		if(show_word_lists):
			top_words = [x[0] for x in self.word_counts.most_common(50)]
			print("50 Most Frequently Occuring Words: ")
			s_words = ', '.join(top_words)
			wrapper = textwrap.TextWrapper(40, break_long_words=False)
			print(wrapper.fill(s_words))

			sw_words = ''
			for word in top_words:
				if word in self.stopwords:
					sw_words = sw_words + ',' + word
			if len(sw_words)>0:
				print('Stopwords in top 20 word counts:', wrapper.fill(sw_words[1:]))
			else:
				print('No stopwords in top 20 most occuring words')
#	def save_to_disc(self):
#		outFile = 
#		for word in self.vocab:



#region		
# If for some reason you cannot run from command line arguments
# edit these variables to path for their respective locations.
d_preprocess = "src/preprocess/"
d_path_data = d_preprocess + "NLP CORPUS TXT/"
d_out_path = d_path_data
f_path_stopwords = d_preprocess + "stopwords.txt"

if len(sys.argv) > 1:
	d_path_data = sys.argv[1]
if len(sys.argv) > 2:
	f_path_stopwords = sys.argv[2]

print("Path Locations: ")
print("\tData Path: ", (pathlib.Path(d_path_data).absolute() ))
print("\tStopwords File Path:", (pathlib.Path(((f_path_stopwords))).absolute()))
#endregion
#pr = cProfile.Profile()
#pr.enable()

model = d_model(d_path_data, out_path=d_out_path)
model.process()
print("Post Processing")
model.report()

initTokens = model.total_word_counts
initVocab = len(model.vocab)

model.sliceCorpusEnds(percentage=0.10)
print("Post Slice")
model.report(show_word_lists=True)
print("Removed", str(initTokens - model.total_word_counts), "tokens and " + \
	 str(initVocab - len(model.vocab)) + " vocab words")

#pr.print_stats(sort='time')
#pr.disable()