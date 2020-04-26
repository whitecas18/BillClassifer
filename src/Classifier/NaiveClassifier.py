from __future__ import division  # this line is important to avoid unexpected behavior from division
import os
import math
from collections import defaultdict, Counter
from gensim.parsing.preprocessing import remove_stopwords

PATH_TO_DATA = os.getcwd()   # path to the data directory
FIRE_LABEL = 'fire'
GOV_LABEL = 'gov'
ENVIRO_LABEL = 'enviro'
HEALTH_LABEL = 'health'
TRAIN_DIR = os.path.join(PATH_TO_DATA, "train")
TEST_DIR = os.path.join(PATH_TO_DATA, "test")


#Tokenizes a document or string
def tokenize_doc(doc):

    bow = defaultdict(float)
    stopTokens = remove_stopwords(doc)
    tokens = stopTokens.split()
    lowered_tokens = map(lambda t: t.lower(), tokens)
    
    for token in lowered_tokens:
        bow[token] += 1.0
    return dict(bow)

#number of word types in word counts
def n_word_types(word_counts):
    
    return len(word_counts)

#number of word tokens in word counts
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
        #self.report_statistics_after_training()
    '''
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
    '''
    def update_model(self, bow, label):
      
      
        for k,v in bow.items():
            self.class_word_counts[label][k] += v
            self.vocab.add(k)

        self.class_total_word_counts[label] = sum(self.class_word_counts[label].values())
        self.class_total_doc_counts[label] += 1

       
    #tokenizes and updates the model
    def tokenize_and_update_model(self, doc, label):
        
        stopTokens = remove_stopwords(doc)
        bow = tokenize_doc(stopTokens)
        self.update_model(bow, label)
      
        

    #returns top number of words in a label
    def top_n(self, label, n):
        
        return Counter(self.class_word_counts[label]).most_common(n)

        
    
    #probability of word given a label
    def p_word_given_label(self, word, label):

        return ((self.class_word_counts[label][word]) / (self.class_total_word_counts[label]))
    
    
    #probability of word given a word and alpha
    def p_word_given_label_and_alpha(self, word, label, alpha):

        return ((self.class_word_counts[label][word] + alpha) / (self.class_total_word_counts[label]))

        
        
    #log of likelihood
    def log_likelihood(self, bow, label, alpha):

        sumNaive = 0

        for k in bow:
            sumNaive += math.log(self.p_word_given_label_and_alpha(k, label, alpha))

        return sumNaive

        
    #log prior
    def log_prior(self, label):
        
        result = 0;
        totDocCount = 0;

        for k in self.class_total_doc_counts:
            totDocCount += self.class_total_doc_counts[k]

        return math.log(self.class_total_doc_counts[label]) / math.log(totDocCount)



    #log posterior unnormalized
    def unnormalized_log_posterior(self, bow, label, alpha):

        return (self.log_prior(label) + self.log_likelihood(bow, label, alpha))



    #classifies a document into one of four labels     
    def classify(self, bow, alpha):
            
        fireClassPos = self.unnormalized_log_posterior(bow, FIRE_LABEL, alpha)
        govClassPos = self.unnormalized_log_posterior(bow, GOV_LABEL, alpha)
        enviroClassPos = self.unnormalized_log_posterior(bow, ENVIRO_LABEL, alpha)
        healthClassPos = self.unnormalized_log_posterior(bow, HEALTH_LABEL, alpha)
        
        classDict = {fireClassPos:FIRE_LABEL, govClassPos:GOV_LABEL, enviroClassPos:ENVIRO_LABEL,healthClassPos:HEALTH_LABEL}
        maxLabel = max(fireClassPos,govClassPos,enviroClassPos,healthClassPos)
        return classDict[maxLabel]

    #evaluates the accuracy of classifier
    def evaluate_classifier_accuracy(self, alpha):
      
        """
        DO NOT MODIFY THIS FUNCTION

        alpha - pseudocount parameter.
        This function should go through the test data, classify each instance and
        compute the accuracy of the classifier (the fraction of classifications
        the classifier gets right.
        """
        correct = 0.0
        total = 0.0

        enviro_path = os.path.join(self.test_dir, ENVIRO_LABEL)
        health_path = os.path.join(self.test_dir, HEALTH_LABEL)
        fire_path = os.path.join(self.test_dir, FIRE_LABEL)
        gov_path = os.path.join(self.test_dir, GOV_LABEL)
        
        
        for (p, label) in [ (enviro_path, ENVIRO_LABEL), (health_path, HEALTH_LABEL),(fire_path, FIRE_LABEL), (gov_path, GOV_LABEL)]:
            for f in os.listdir(p):
                with open(os.path.join(p,f),'r') as doc:
                    content = doc.read()
                    bow = self.tokenize_doc(content)
                    if self.classify(bow, alpha) == label:
                        correct += 1.0
                    total += 1.0
        return 100 * correct / total


