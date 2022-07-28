import sys
from sklearn.metrics import classification_report
from sqlalchemy import create_engine
from sklearn.multioutput import MultiOutputClassifier
from sklearn.multiclass import OneVsRestClassifier
from sklearn.model_selection import GridSearchCV
import nltk
nltk.download(['punkt', 'wordnet'])
nltk.download('stopwords')
import numpy as np
import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import pickle
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn import svm
from lightgbm import LGBMClassifier
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.model_selection import train_test_split
import re

def load_data(database_filepath):
    engine = create_engine('sqlite:///' + str(database_filepath))
    df = pd.read_sql_table("disaster", con=engine)
    print(df.columns)
    X = df['message']
    Y = df.iloc[:,4:]
    print(Y)
    return X, Y, df.columns


def tokenize(text):
    stop_words = stopwords.words()
    text = text.lower()
    text = re.sub(r"[^a-zA-Z0-9]"," ",text)
    tokens = word_tokenize(text)
    words = [WordNetLemmatizer().lemmatize(t) for t in tokens if t.lower().strip() not in stop_words]
    return words


def build_model():
    pipeline = Pipeline([
    ('vect', CountVectorizer(tokenizer=tokenize)),
    ('tfidf', TfidfTransformer()),
    ('clf', MultiOutputClassifier(LGBMClassifier()))
    #('clf', MultiOutputClassifier(svm.SVC()))
    ])

    parameters = {
        #...
        
    }

    cv = GridSearchCV(pipeline, param_grid = parameters)
    return cv

def evaluate_model(model, X_test, Y_test, category_names):
    print(classification_report(Y_test, model.predict(X_test)))


def save_model(model, model_filepath):
    pickle.dump(model, open(model_filepath,'wb'))


def main():
    if len(sys.argv) == 3:
        database_filepath, model_filepath = sys.argv[1:]
        print('Loading data...\n    DATABASE: {}'.format(database_filepath))
        X, Y, category_names = load_data(database_filepath)
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.1)
        
        print('Building model...')
        model = build_model()
        
        print('Training model...')
        model.fit(X_train, Y_train)
        
        print('Evaluating model...')
        evaluate_model(model, X_test, Y_test, category_names)

        print('Saving model...\n    MODEL: {}'.format(model_filepath))
        save_model(model, model_filepath)

        print('Trained model saved!')

    else:
        print('Please provide the filepath of the disaster messages database '\
              'as the first argument and the filepath of the pickle file to '\
              'save the model to as the second argument. \n\nExample: python '\
              'train_classifier.py ../data/DisasterResponse.db classifier.pkl')


if __name__ == '__main__':
    main()
