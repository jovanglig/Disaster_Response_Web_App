import json
import plotly
import pandas as pd


from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from flask import render_template, request, jsonify
from plotly.graph_objs import Bar, Pie
from sqlalchemy import create_engine
import joblib
from app import app






def tokenize(text):
    tokens = word_tokenize(text)
    lemmatizer = WordNetLemmatizer()

    clean_tokens = []
    for tok in tokens:
        clean_tok = lemmatizer.lemmatize(tok).lower().strip()
        clean_tokens.append(clean_tok)

    return clean_tokens

# load data
engine = create_engine('sqlite:///../data/DisasterResponse.db')
df = pd.read_sql_table('messages', engine)


# load model
model = joblib.load("../models/classifier.pkl")
# load predictions & y_test
data = joblib.load("../models/cat_accuracy.pkl")
accuracy = data['accuracy'] 



# index webpage displays cool visuals and receives user input text for model
@app.route('/')
@app.route('/index')
def index():
    
    # extract data needed for visuals
    # TODO: Below is an example - modify to extract data for your own visuals
    genre_counts = df.groupby('genre').count()['message']
    genre_names = list(genre_counts.index)
    Y = df.iloc[:,4:]
    category_names = Y.columns[1:]
    category_counts = [df[x].sum() for x in category_names]
    related_counts = df.groupby('related').count()['message']
    related_counts.index = ['Not related', 'Related', 'Urgent']
    related_names = list(related_counts.index)
    
    
    # create visuals
    # TODO: Below is an example - modify to create your own visuals
    graphs = [
        {
            'data': [
                Bar(
                    x=genre_names,
                    y=genre_counts
                )
            ],

            'layout': {
                'title': 'Distribution of Message Genres',
                'yaxis': {
                    'title': "Count"
                },
                'xaxis': {
                    'title': "Genre"
                }
            }
        },
        {
            'data': [
                Pie(
                    labels=related_names,
                    values=related_counts,
                    hole = .5,
                    textinfo='label+percent',
                    pull=[0, 0, 0.2]
                    
                )
            ],

            
        },
        
        {
            'data': [
                Bar(
                    x=category_names,
                    y=category_counts
                    
                )
            ],

            'layout': {
                'title': 'Distribution of Message Categories',
                'yaxis': {
                    'title': "Count"
                },
                'xaxis': {
                    'title': "Category",
                    
                },
                
            }
        },
        {
            'data': [
                Bar(
                    x=list(accuracy.index),
                    y=accuracy.values
                    
                )
            ],
            
            'layout': {
                'title': 'Classification Accuracy of Message Categories',
                'yaxis': {
                    'title': "Accuracy in %"
                },
                'xaxis': {
                    'title': "Category",
                    
                }
            }
            
        },
    ]
    
       
    
    
    # encode plotly graphs in JSON
    ids = ["graph-{}".format(i) for i, _ in enumerate(graphs)]
    graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)
    
    # render web page with plotly graphs
    return render_template('master.html', ids=ids, graphJSON=graphJSON)


# web page that handles user query and displays model results
@app.route('/go')
def go():
    # save user input in query
    query = request.args.get('query', '') 

    # use model to predict classification for query
    classification_labels = model.predict([query])[0]
    classification_results = dict(zip(df.columns[4:], classification_labels))

    # This will render the go.html Please see that file. 
    return render_template(
        'go.html',
        query=query,
        classification_result=classification_results
    )



#def main():
 #   app.run(host='0.0.0.0', port=3001, debug=True)


#if __name__ == '__main__':
#    main()

