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
# -- UPDATE documents SET  model_embedding_cos = model_embedding1 <=> model_embedding2;
# -- UPDATE documents SET  question_embedding_cos = embedding1 <=> embedding2;

logging.basicConfig(level=logging.DEBUG)

class db:

    def __init__(self):
        logging.debug('db.init')

        current_GMT = time.gmtime()
        time_stamp = calendar.timegm(current_GMT)

        config = configparser.RawConfigParser()   
        configFilePath = r'/nas/projects/EMSE6900/src/configuration.txt'
        config.read(configFilePath)

        self.rdbms = config.get('kandinsky', 'rdbms')
        self.username = config.get('kandinsky', 'username')
        self.password = config.get('kandinsky', 'password')
        self.host = config.get('kandinsky', 'host')
        self.port = config.get('kandinsky', 'port')
        self.database = config.get('kandinsky', 'database')
        self.table = config.get('kandinsky', 'table')

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

        logging.debug('db.query')

        sql='SELECT * FROM ' + self.table + ' WHERE (model_response1 NOT LIKE \'Sorry%\') and (model_response2 NOT LIKE \'Sorry%\') and (experiment_id = ' + str(experiment_id) + ')'

        logging.debug(sql)

        try:
            
            engine = create_engine(self.rdbms + '://' + self.username + ':' + self.password +'@' + self.host + '/' + self.database)

            with engine.begin() as conn:

                # select all rows of the database that contain experiment_id of a specific value
                df = pd.read_sql_query(sql=text(sql), con = conn)
                logging.debug("Record selected successfully from table " + self.table)
                return df

        except (Exception, psycopg2.Error) as error:
            logging.error("Failed to select record from table " + self.table, error)