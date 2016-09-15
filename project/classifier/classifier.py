import cPickle as pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cross_validation import train_test_split
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
from sklearn.svm import SVC
from time import time

LINK_FILES = ["rotten.txt", "imdb.txt", "metacritic.txt", "movies.txt", "allmovies.txt", "flixter.txt", "tribute.txt", "boxofficemojo.txt", "mubi.txt", "yifi.txt"]
DATABASE = "database/database.pickle"

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

def print_scores(scores):
    print "Accuracy: %f" % scores['accuracy']
    print "Precision: %f" % scores['precision']
    print "Recall: %f" % scores['recall']
    print "F1-Measure: %f\n" % scores['f1']

def try_svm(features_train, features_test, labels_train, labels_test):
    print "Testing SVMs:"

    C = [1, 10, 20, 100, 1000, 10000]
    kernels = ['rbf', 'linear', 'poly', 'sigmoid']

    for c in C:
        for kernel in kernels:
            print "C=%d, kernel=%s" % (c, kernel)

            t0 = time()
            clf = SVC(C=c, kernel=kernel)
            clf.fit(features_train, labels_train)
            print "Training time %fs" % round(time() - t0, 3)

            scores = evaluate(labels_test, clf.predict(features_test))
            print_scores(scores)

def try_mlp(features_train, features_test, labels_train, labels_test):
    #TODO
    pass

def try_random_forest(features_train, features_test, labels_train, labels_test):
    #TODO
    pass

def try_regression(features_train, features_test, labels_train, labels_test):
    #TODO
    pass

if __name__ == '__main__':
    db = load_database()
    X, Y = prepare_database(db)

    bag_of_words, bag_of_words_vectors = create_bag_of_words(X)
    tfidf, tfidf_vectors = create_TfIdf(X)

    features_train, features_test, labels_train, labels_test = split_dataset(bag_of_words_vectors, Y)

    try_svm(features_train, features_test, labels_train, labels_test)
