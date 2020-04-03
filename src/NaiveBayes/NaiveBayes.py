from __future__ import division  # this line is important to avoid unexpected behavior from division
import os
import zipfile
import math
import time
import operator
from collections import defaultdict, Counter

PATH_TO_DATA = os.getcwd()   # path to the data directory
FIRE_LABEL = 'fire'
GOV_LABEL = 'gov'
ENVIRO_LABEL = 'enviro'
HEALTH_LABEL = 'health'
TRAIN_DIR = os.path.join(PATH_TO_DATA, "train")
TEST_DIR = os.path.join(PATH_TO_DATA, "test")



def tokenize_doc(doc):

    bow = defaultdict(float)
    tokens = doc.split()
    lowered_tokens = map(lambda t: t.lower(), tokens)
    for token in lowered_tokens:
        bow[token] += 1.0
    return dict(bow)



def n_word_types(word_counts):
    
    return len(word_counts)


def n_word_tokens(word_counts):

    counter = 0;

    for keys in word_counts:
        counter += word_counts.get(keys)
        
    return counter


###### NAIVE BAYES BLOCK ######

class NaiveBayes:
    
    """A Naive Bayes model for text classification."""

    def __init__(self, path_to_data, tokenizer):
        # Vocabulary is a set that stores every word seen in the training data
        self.vocab = set()
        self.path_to_data = path_to_data
        self.tokenize_doc = tokenizer
        self.train_dir = os.path.join(path_to_data, "train")
        self.test_dir = os.path.join(path_to_data, "test")
        # class_total_doc_counts is a dictionary that maps a class (i.e., pos/neg) to
        # the number of documents in the trainning set of that class
        self.class_total_doc_counts = { FIRE_LABEL: 0.0,
                                        GOV_LABEL: 0.0, 
                                        ENVIRO_LABEL: 0.0,
                                        HEALTH_LABEL: 0.0}                

        # class_total_word_counts is a dictionary that maps a class (i.e., pos/neg) to
        # the number of words in the training set in documents of that class
        self.class_total_word_counts = { FIRE_LABEL: 0.0,
                                        GOV_LABEL: 0.0, 
                                        ENVIRO_LABEL: 0.0,
                                        HEALTH_LABEL: 0.0} 

        # class_word_counts is a dictionary of dictionaries. It maps a class (i.e.,
        # pos/neg) to a dictionary of word counts. For example:
        #    self.class_word_counts[POS_LABEL]['awesome']
        # stores the number of times the word 'awesome' appears in documents
        # of the positive class in the training documents.
        self.class_word_counts = { FIRE_LABEL: defaultdict(float),
                                   GOV_LABEL: defaultdict(float),
                                   ENVIRO_LABEL: defaultdict(float),
                                   HEALTH_LABEL: defaultdict(float) }

    def train_model(self):
        """
        This function processes the entire training set using the global PATH
        variable above.  It makes use of the tokenize_doc and update_model
        functions you will implement.
        """

        fire_path = os.path.join(self.train_dir, FIRE_LABEL)
        gov_path = os.path.join(self.train_dir, GOV_LABEL)
        enviro_path = os.path.join(self.train_dir, ENVIRO_LABEL)
        health_path = os.path.join(self.train_dir, HEALTH_LABEL)
        
        for (p, label) in [ (fire_path, FIRE_LABEL), (gov_path, GOV_LABEL), (enviro_path, ENVIRO_LABEL), (health_path, HEALTH_LABEL) ]:
            for f in os.listdir(p):
                with open(os.path.join(p,f),'r',encoding="utf8") as doc:
                    content = doc.read()
                    self.tokenize_and_update_model(content, label)
        self.report_statistics_after_training()

    def report_statistics_after_training(self):
        """
        Report a number of statistics after training.
        """

        print ("REPORTING CORPUS STATISTICS")
        print ("NUMBER OF DOCUMENTS IN FIREARMS CLASS:", self.class_total_doc_counts[FIRE_LABEL])
        print ("NUMBER OF DOCUMENTS IN GOVERNMENT CLASS:", self.class_total_doc_counts[GOV_LABEL])
        print ("NUMBER OF DOCUMENTS IN ENVIRONMENT CLASS:", self.class_total_doc_counts[ENVIRO_LABEL])
        print ("NUMBER OF DOCUMENTS IN HEALTH CLASS:", self.class_total_doc_counts[HEALTH_LABEL])
        print ("NUMBER OF TOKENS IN FIREARMS CLASS:", self.class_total_word_counts[FIRE_LABEL])
        print ("NUMBER OF TOKENS IN GOVERNMENT CLASS:", self.class_total_word_counts[GOV_LABEL])
        print ("NUMBER OF TOKENS IN ENVIRONMENT CLASS:", self.class_total_word_counts[ENVIRO_LABEL])
        print ("NUMBER OF TOKENS IN HEALTH CLASS:", self.class_total_word_counts[HEALTH_LABEL])
        print ("VOCABULARY SIZE: NUMBER OF UNIQUE WORDTYPES IN TRAINING CORPUS:", len(self.vocab))

    def update_model(self, bow, label):
      
      
        for k,v in bow.items():
            self.class_word_counts[label][k] += v
            self.vocab.add(k)

        self.class_total_word_counts[label] = sum(self.class_word_counts[label].values())
        self.class_total_doc_counts[label] += 1

      
    
        
        

    def tokenize_and_update_model(self, doc, label):
        bow = tokenize_doc(doc)
        self.update_model(bow, label)
      
        


    def top_n(self, label, n):
        
        return Counter(self.class_word_counts[label]).most_common(n)

        
    

    def p_word_given_label(self, word, label):

        return ((self.class_word_counts[label][word]) / (self.class_total_word_counts[label]))
    


    def p_word_given_label_and_alpha(self, word, label, alpha):

        return ((self.class_word_counts[label][word] + alpha) / (self.class_total_word_counts[label]))

        
        

    def log_likelihood(self, bow, label, alpha):

        sumNaive = 0

        for k in bow:
            sumNaive += math.log(self.p_word_given_label_and_alpha(k, label, alpha))

        return sumNaive

        

    def log_prior(self, label):
        
        result = 0;
        totDocCount = 0;

        for k in self.class_total_doc_counts:
            totDocCount += self.class_total_doc_counts[k]

        return math.log(self.class_total_doc_counts[label]) / math.log(totDocCount)




    def unnormalized_log_posterior(self, bow, label, alpha):

        return (self.log_prior(label) + self.log_likelihood(bow, label, alpha))



        
    def classify(self, bow, alpha):
            
        fireClassPos = self.unnormalized_log_posterior(bow, FIRE_LABEL, alpha)
        govClassPos = self.unnormalized_log_posterior(bow, GOV_LABEL, alpha)
        enviroClassPos = self.unnormalized_log_posterior(bow, ENVIRO_LABEL, alpha)
        healthClassPos = self.unnormalized_log_posterior(bow, HEALTH_LABEL, alpha)
        
        classDict = {FIRE_LABEL:fireClassPos, GOV_LABEL:govClassPos, ENVIRO_LABEL: enviroClassPos,HEALTH_LABEL:healthClassPos}
        return max(classDict.iteritems(), key=operator.itemgetter(1))[0]



nb = NaiveBayes(PATH_TO_DATA, tokenizer=tokenize_doc)
nb.train_model()

print ("TOP 10 WORDS FOR CLASS " + FIRE_LABEL + ":")
for tok, count in nb.top_n(FIRE_LABEL, 10):
    print ('', tok, count)
print ()

print ("TOP 10 WORDS FOR CLASS " + GOV_LABEL + ":")
for tok, count in nb.top_n(GOV_LABEL, 10):
    print ('', tok, count)
print ()

print ("TOP 10 WORDS FOR CLASS " + ENVIRO_LABEL + ":")
for tok, count in nb.top_n(ENVIRO_LABEL, 10):
    print ('', tok, count)
print ()

print ("TOP 10 WORDS FOR CLASS " + HEALTH_LABEL + ":")
for tok, count in nb.top_n(HEALTH_LABEL, 10):
    print ('', tok, count)
print ()