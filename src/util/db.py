import calendar
import configparser
import logging
import pandas as pd
import psycopg2
import time
from sqlalchemy import create_engine, text
import logging

# uses https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_sql.html
# After run 

# pgvector <=> is cosine distance, not cosine similarity
# https://github.com/supabase/supabase/issues/12244

# -- UPDATE documents SET  model_embedding_cos =  abs((model_embedding1 <=> model_embedding2) - 1);
# -- UPDATE documents SET  question_embedding_cos = abs((question_embedding1 <=> question_embedding2) - 1);

logging.basicConfig(level=logging.ERROR)
#logging.basicConfig(level=logging.DEBUG)

class db:

    def __init__(self, server):
        logging.debug('db.init')

        current_GMT = time.gmtime()
        time_stamp = calendar.timegm(current_GMT)

        config = configparser.RawConfigParser()   
        #configFilePath = r'N:/projects/EMSE6900/src/configuration.txt'
        configFilePath = r'/nas/projects/EMSE6900/src/configuration.txt'
        config.read(configFilePath)

        #server  = 'basquiat'
        #server  = 'kandinsky'

        self.rdbms = config.get(server, 'rdbms')
        self.username = config.get(server, 'username')
        self.password = config.get(server, 'password')
        self.host = config.get(server, 'host')
        self.port = config.get(server, 'port')
        self.database = config.get(server, 'database')
        self.table = config.get(server, 'table')

    def insert_data_frame(self, df):

        logging.debug('db.insert')

        try:
            engine = create_engine(self.rdbms + '://' + self.username + ':' + self.password +'@' + self.host + '/' + self.database)
            test = df.to_sql(name=self.table, con=engine, if_exists = 'append', index=False)
            print(test)
            logging.debug("Record inserted successfully into table " + self.table)

        except (Exception, psycopg2.Error) as error:
            logging.error("Failed to insert record into table " + self.table, error)

    def query(self, experiment_id):

        logging.debug('db.query to ' + experiment_id )

        #sql='SELECT * FROM ' + self.table + ' WHERE experiment_id = ' + str(experiment_id) + ')'
        sql='SELECT * FROM ' + self.table + ' WHERE ((model_response1 NOT LIKE \'%Sorry%\') AND (model_response2 NOT LIKE \'%Sorry%\')) and (experiment_id = ' + str(experiment_id) + ')'

        logging.error(sql)

        try:
            
            engine = create_engine(self.rdbms + '://' + self.username + ':' + self.password +'@' + self.host + '/' + self.database)

            with engine.begin() as conn:

                # select all rows of the database that contain experiment_id of a specific value
                df = pd.read_sql_query(sql=text(sql), con = conn)
                logging.debug("Record selected successfully from table " + self.table)
                print(df['model_response1'])
                return df

        except (Exception, psycopg2.Error) as error:
            logging.error("Failed to select record from table " + self.table, error)