# imports
from util import db as database
import os
import pandas as pd
import calendar
import time 
import pickle


#with open('/nas/projects/EMSE6900/data/response.pkl', 'rb') as f:
#    response = pickle.load(f)
#print(response)
server = 'basquiat'
df = pd.read_pickle(r'C:/Users/bnreed/projects/semantics/data/dataframe_1692850565.pkl')
df = df.drop(columns=['id'])

# df['model_response1'] = df['model_response1'].apply(lambda x: x.replace('"', ''))
# df['model_response1'] = df['model_response1'].apply(lambda x: x.replace('\n', ''))
# df['model_response1'] = df['model_response1'].apply(lambda x: x.replace("'", ""))

# df['model_response2'] = df['model_response2'].apply(lambda x: x.replace('"', ''))
# df['model_response2'] = df['model_response2'].apply(lambda x: x.replace('\n', ''))
# df['model_response2'] = df['model_response2'].apply(lambda x: x.replace("'", ""))

print(df.head())
print(df.shape)

for col in df.columns:
    print(col)

#current_GMT = time.gmtime()
#time_stamp = calendar.timegm(current_GMT)


mydb = database.db(server)
mydb.insert_data_frame(df)

