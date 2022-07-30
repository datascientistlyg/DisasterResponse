import sys
import pandas as pd
from sqlalchemy import create_engine

def load_data(messages_filepath, categories_filepath):
    '''
    Load data from csv files and merge into dataframe
    
    INPUTS:
        messages_filepath : messages file path
        categories_filepath : categories file path
    RETURNS:
        df : merged dataframe
    '''
    
    m = pd.read_csv(messages_filepath)
    c = pd.read_csv(categories_filepath)
    #c = c['categories'].str.split(';', expand = True)
    df = pd.merge(m,c)
    df_s = df['categories'].str.split(';', expand = True)
    print(df_s.head(10))
    df_s.columns = df_s.iloc[0,:].apply(lambda x:x[:-2])
    for c in df_s:
        df_s[c] = df_s[c].str[-1].astype(int)
    df_s = df_s.clip(0,1) #binary        
    print("-------")
    print(df_s.columns)
    df = pd.concat([df, df_s], axis=1).drop(columns=['categories'])
    return df


def clean_data(df):
    '''
    Clean the dataframe and drop the duplicates
    
    INPUTS:
        df : input dataframe
    RETURNS:
        df : cleaned dataframe
    '''
    
    df = df.drop_duplicates()
    return df


def save_data(df, database_filename):
    '''
    Save the dataframe to database
    
    INPUTS:
        df : input dataframe
        database_filename : the database filename which the dataframe will be stored to 

    '''

    db_engine = create_engine('sqlite:///'+database_filename)
    conn = db_engine.connect()
    df.to_sql('disaster', db_engine, index=False, if_exists='replace')
    conn.close()


def main():
    if len(sys.argv) == 4:

        messages_filepath, categories_filepath, database_filepath = sys.argv[1:]

        print('Loading data...\n    MESSAGES: {}\n    CATEGORIES: {}'
              .format(messages_filepath, categories_filepath))
        df = load_data(messages_filepath, categories_filepath)

        print('Cleaning data...')
        df = clean_data(df)
        
        print('Saving data...\n    DATABASE: {}'.format(database_filepath))
        save_data(df, database_filepath)
        
        print('Cleaned data saved to database!')
    
    else:
        print('Please provide the filepaths of the messages and categories '\
              'datasets as the first and second argument respectively, as '\
              'well as the filepath of the database to save the cleaned data '\
              'to as the third argument. \n\nExample: python process_data.py '\
              'disaster_messages.csv disaster_categories.csv '\
              'DisasterResponse.db')


if __name__ == '__main__':
    main()
