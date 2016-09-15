import cPickle as pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer

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

if __name__ == '__main__':
    db = load_database()
    X, Y = prepare_database(db)
    bag_of_words, bag_of_words_vectors = create_bag_of_words(X)
    tfidf, tfidf_vectors = create_TfIdf(X)
