# Disaster Response Pipeline Project

### Description
This repo contains files that pertain to the Disaster Response Pipeline Project from Udacity's Data Scientist Nanodegree programme.
This project uses disaster data from Figure Eight to build a model for an API that classifies disaster messages.
The data contains real messages that were sent during disaster events. 
I have created a machine learning pipeline using scikit-learn to categorize these messages/events into 36 categories so that they may be sent to an appropriate disaster relief agency.
The project also includes a web app where an emergency worker can input a new message and get classification results in several categories. 
The web app will also display visualizations of the data.

### Summary
The model has an average accuracy accross categories of about 94%. The model is a Random Forest Classifier and uses tokenized words transformed to get TF-IDF counts. 
Grid Search was used as well to find the best possible parameters for the model. 

### Files
The data folder contains the messages and categories data including the ETL pipeline script and the data stored in a database.
The models folder contains the model script as well as pickle files which store the model and accuracy score in binary format.
The app folder contains the html pages and the run.py which uses the model and reads the data from the database and subsequently runs the webapp with the visualizations using plotly and flask.


### Packages used
- plotly
- flask
- json
- sys
- numpy
- pandas
- scikit-learn
- pickle
- joblib
- nltk
- sqlalchemy


### Instructions:
1. Run the following commands in the project's root directory to set up the database and model.

    - To run ETL pipeline that cleans data and stores in database
        `python data/process_data.py data/disaster_messages.csv data/disaster_categories.csv data/DisasterResponse.db`
    - To run ML pipeline that trains classifier and saves
        `python models/train_classifier.py data/DisasterResponse.db models/classifier.pkl`

2. Run the following command in the main directory to run the web app.
    `python app/run.py`

3. Go to http://0.0.0.0:3001/. 
