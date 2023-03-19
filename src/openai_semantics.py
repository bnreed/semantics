# https://github.com/openai/openai-cookbook/blob/5b5f22812158002f19e24fcb5c9a391a6551c1e2/examples/Obtain_dataset.ipynb
# https://github.com/openai/openai-cookbook/blob/main/examples/Question_answering_using_embeddings.ipynb

# imports
import calendar
from util import db as database
import os
import pandas as pd
import pickle
import sqlalchemy
import tiktoken
import time
import openai
from openai.embeddings_utils import get_embedding

from tenacity import retry, wait_random_exponential, stop_after_attempt

prime = "Answer the question as truthfully as possible, and if you're unsure of the answer, say 'Sorry, I don't know'. "

# embedding model parameters
COMPLETIONS_MODEL = "text-davinci-003"
EMBEDDING_MODEL = "text-embedding-ada-002"

embedding_encoding = "cl100k_base"  # this the encoding for text-embedding-ada-002
max_tokens = 200  # the maximum for text-embedding-ada-002 is 8191

# load & inspect dataset
input_datapath = "data/questions.csv"  
pickle_dir = "data/"
df = pd.read_csv(input_datapath) #, index_col=0)
#df = df["id", "qid1", "qid2", "question1", "question2", "is_duplicate"]
df = df.dropna()

#test debug against a small set
df = df.sample(n=5, random_state=1)

encoding = tiktoken.get_encoding(embedding_encoding)

print(df)



# omit reviews that are too long to embed
#df["n_tokens"] = df.combined.apply(lambda x: len(encoding.encode(x)))
#df = df[df.n_tokens <= max_tokens].tail(top_n)
#len(df)

#@retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(6))
#def get_embedding(text) -> list[float]:
#    return openai.Embedding.create(input=text, model=embedding_model)["data"][0]["embedding"]

@retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(6))
def get_response(text, model) -> list[str]:
    # send a Completion request to count to 100
    response = openai.Completion.create(
        model=model,
        #prompt = prime + " " + text,
        prompt = text,
        max_tokens=200,
        temperature=0,
    )
    #response = openai.Answer.create(model=embedding_model, question=text, max_tokens=50, temperature=0)

    outfile = pickle_dir + 'response.pkl'
    with open(outfile, 'wb') as pickle_file:
        pickle.dump(response, pickle_file)

    return response['choices'][0]['text']

df['embedding1'] = df.apply(lambda x: get_embedding(x['question1'], engine=EMBEDDING_MODEL), axis=1)
df['embedding2'] = df.apply(lambda x: get_embedding(x['question2'], engine=EMBEDDING_MODEL), axis=1)
print(df)
df['model_response1'] = df.apply(lambda x: get_response(x['question1'], model=COMPLETIONS_MODEL), axis=1)
df['model_response2'] = df.apply(lambda x: get_response(x['question2'], model=COMPLETIONS_MODEL), axis=1)
print(df)
df['model_embedding1'] = df.apply(lambda x: get_embedding(x['model_response1'], engine=EMBEDDING_MODEL), axis=1)
df['model_embedding2'] = df.apply(lambda x: get_embedding(x['model_response2'], engine=EMBEDDING_MODEL), axis=1)
print(df)
current_GMT = time.gmtime()
time_stamp = calendar.timegm(current_GMT)

# incase of sql error
df.to_pickle(pickle_dir + os.sep + 'dataframe_' + str(time_stamp) + '.pkl')

df["experiment_id"] = time_stamp

print(df.head())
print(df.shape)

mydb = database.db()
mydb.insert_data_frame(df)




