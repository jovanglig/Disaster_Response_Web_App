import sys
import pandas as pd
<<<<<<< HEAD
=======
import re
>>>>>>> 01f921e5fb56693c4c7389f266efb432eb094cd2
import numpy as np
from sqlalchemy import create_engine
import nltk
nltk.download(['punkt', 'wordnet'])
from nltk.tokenize import word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.multioutput import MultiOutputClassifier
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.model_selection import GridSearchCV
import pickle

def load_data(database_filepath):
    engine = create_engine('sqlite:///'+database_filepath)
    df = pd.read_sql_table('messages', engine )
    X = df['message'].values
    Y = df.iloc[:,4:]
    category_names = Y.columns
    return X, Y, category_names

def tokenize(text):
    tokens = word_tokenize(text)
    lemmatizer = WordNetLemmatizer()

    clean_tokens = []
    for tok in tokens:
        clean_tok = lemmatizer.lemmatize(tok).lower().strip()
        clean_tokens.append(clean_tok)

    return clean_tokens


def build_model():
    pipeline = Pipeline([
    
        ('features', FeatureUnion([

                ('text_pipeline', Pipeline([
                    ('vect', CountVectorizer(tokenizer=tokenize)),
                    ('tfidf', TfidfTransformer())
                ])),


            ])),

        ('clf', MultiOutputClassifier(RandomForestClassifier(random_state = 42))),
    
    ])
    
    parameters = {'features__text_pipeline__vect__ngram_range': ((1, 1), (1, 2)),
    #'features__text_pipeline__vect__max_df': (0.5, 0.75, 1.0),
    #'features__text_pipeline__vect__max_features': (None, 5000, 10000),
    #'features__text_pipeline__tfidf__use_idf': (True, False),
    #'clf__estimator__n_estimators': [50, 100, 200],
    #'clf__estimator__min_samples_split': [2, 3, 4],
    
    
    }

    cv = GridSearchCV(pipeline, param_grid = parameters)
    return cv
    
    
def evaluate_model(model, X_test, Y_test, category_names):
    y_pred = model.predict(X_test)
    accuracy = (Y_test == y_pred).mean().mean()
    category_accuracy = (Y_test == y_pred).mean()
    print("Accuracy:", accuracy)
    y_pred = np.transpose(y_pred)
    for i in range(len(category_names)):
        print(classification_report(Y_test.iloc[:,i], y_pred[i]))
    return category_accuracy
    
def save_model(model, model_filepath, category_accuracy):
    '''
    Args:
    model : model
    model_filepath: filepath to model
    category_accuracy: 
    
    '''
    pickle.dump(model,open(model_filepath,'wb'))
    data = {'accuracy': category_accuracy}
    pickle.dump(data, open("models/cat_accuracy.pkl",'wb'))
    
    
def main():
    if len(sys.argv) == 3:
        database_filepath, model_filepath = sys.argv[1:]
        print('Loading data...\n    DATABASE: {}'.format(database_filepath))
        X, Y, category_names = load_data(database_filepath)
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)
       
        print('Building model...')
        model = build_model()
        
        print('Training model...')
        model.fit(X_train, Y_train)
        
        print('Evaluating model...')
        category_accuracy = evaluate_model(model, X_test, Y_test, category_names)

        print('Saving model...\n    MODEL: {}'.format(model_filepath))
        save_model(model, model_filepath, category_accuracy)

        print('Trained model saved!')

    else:
        print('Please provide the filepath of the disaster messages database '\
              'as the first argument and the filepath of the pickle file to '\
              'save the model to as the second argument. \n\nExample: python '\
              'train_classifier.py ../data/DisasterResponse.db classifier.pkl')


if __name__ == '__main__':
    main()