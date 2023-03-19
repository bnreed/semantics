# imports
import util.db as db
import os
import pandas as pd
import calendar
import time 
import pickle

response = ''
with open('/nas/projects/EMSE6900/data/response.pkl', 'rb') as f:
    response = pickle.load(f)
print(response)

df = pd.read_pickle(r'/nas/projects/EMSE6900/data/dataframe_1678058582.pkl')

df['model_response1'] = df['model_response1'].apply(lambda x: x.replace('"', ''))
df['model_response1'] = df['model_response1'].apply(lambda x: x.replace('\n', ''))
df['model_response1'] = df['model_response1'].apply(lambda x: x.replace("'", ""))

df['model_response2'] = df['model_response2'].apply(lambda x: x.replace('"', ''))
df['model_response2'] = df['model_response2'].apply(lambda x: x.replace('\n', ''))
df['model_response2'] = df['model_response2'].apply(lambda x: x.replace("'", ""))

print(df.head())
print(df.shape)

for col in df.columns:
    print(col)

current_GMT = time.gmtime()
time_stamp = calendar.timegm(current_GMT)

df["experiment_id"] = time_stamp



print(df.head())
print(df.shape)

db = db.dbinsert()
resp = db.insert_data_frame(df)

print(resp)