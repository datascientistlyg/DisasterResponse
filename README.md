# DisasterResponse
## Project Description:
This project includes a web app where an emergency worker can input a new message and get classification results in several categories. The web app will also display visualizations of the data. 

This application will greatly impact the community, and this application will help people or organization in an event of a disaster. This model could be used to classify messages and messages could to be sent to the appropriate agencies.  

## File Description:
1. models directory: train_classifier.py
2. data directory: process_data.py
3. app directory: run.py

## File architecture:
- app

|- run.py  # Flask file that runs app

- data

|- disaster_categories.csv  # data to process 

|- disaster_messages.csv  # data to process

|- process_data.py

- models

|- train_classifier.py

- README.md

## Run Instructions:
1. Run the following commands in the project's root directory to set up your database and model.
    - To run ETL pipeline that cleans data and stores in database
        `python data/process_data.py data/disaster_messages.csv data/disaster_categories.csv data/DisasterResponse.db`
    - To run ML pipeline that trains classifier and saves
        `python models/train_classifier.py data/DisasterResponse.db models/classifier.pkl`

2. Go to `app` directory: `cd app`

3. Run your web app: `python run.py`

4. Click the `PREVIEW` button to open the homepage
