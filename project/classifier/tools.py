import re
import os
import cPickle as pickle
from time import time
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cross_validation import train_test_split
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
from nltk.corpus import stopwords
from bs4 import BeautifulSoup

LINK_FILES = ["rotten.txt", "imdb.txt", "metacritic.txt", "movies.txt", "allmovies.txt", "flixter.txt", "tribute.txt", "boxofficemojo.txt", "mubi.txt", "yifi.txt"]

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
DATABASE_FILE = "database/database.pickle"
DATABASE = os.path.join(DIR_PATH, DATABASE_FILE)

def clean_text(text):
	letters_only = re.sub("[^a-zA-Z]", " ", text)
	words = letters_only.lower().split()
	meaningful_words = [w for w in words if not w in STOPWORDS]
	return " ".join(meaningful_words)

def visible(element):
	if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
		return False
	elif re.match('<!--.*-->', str(element.encode('utf-8'))):
		return False
	else:
		return True

def extract_text(html):
	soup = BeautifulSoup(html, 'html.parser')
	data = soup.findAll(text=True)
	all_text = ''.join(filter(visible, data))
	text = all_text.replace('\n', ' ').replace('\r', '').strip()
	text = ' '.join(text.split())
	text = clean_text(text)
	return text

def load_database():
    print "Recovering data from '%s'..." % DATABASE
    f = open(DATABASE, 'rb')
    db = pickle.load(f)
    f.close()
    return db

def prepare_database(database):
    print "Preparing the database..."

    X = []
    Y = []

    for filename in LINK_FILES:
        pages = database[filename]
        for text in pages['positive']:
            X.append(text)
            Y.append(1)
        for text in pages['negative']:
            X.append(text)
            Y.append(0)

    return (X, Y)

def create_bag_of_words(texts):
    vectorizer = CountVectorizer(analyzer = "word", tokenizer = None, preprocessor = None, stop_words = None, max_features = 5000)
    print "Training the Bag Of Words model..."
    train_data_features = vectorizer.fit_transform(texts)
    print "Converting the texts to feature vectors..."
    train_data_features = train_data_features.toarray()
    return (vectorizer, train_data_features)

def create_TfIdf(texts):
    vectorizer = TfidfVectorizer(analyzer = "word", tokenizer = None, preprocessor = None, stop_words = None, max_features = 5000)
    print "Training the Tf Idf model..."
    train_data_features = vectorizer.fit_transform(texts)
    print "Converting the texts to feature vectors..."
    train_data_features = train_data_features.toarray()
    return (vectorizer, train_data_features)

def split_dataset(X, Y):
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.33, random_state=42)
    return (X_train, X_test, y_train, y_test)

def evaluate(Y_true, Y_pred):
    acc_score = accuracy_score(Y_true, Y_pred)
    prec_score = precision_score(Y_true, Y_pred)
    rec_score = recall_score(Y_true, Y_pred)
    f_score = f1_score(Y_true, Y_pred)
    return {'accuracy': acc_score, 'precision': prec_score, 'recall': rec_score, 'f1': f_score}
