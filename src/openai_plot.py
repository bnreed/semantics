from util import db
import configparser
import os
import pandas as pd
import pickle
from util import db as database
import logging
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style='ticks')

config = configparser.RawConfigParser()   
configFilePath = r'/nas/projects/EMSE6900/src/configuration.txt'
#configFilePath = r'N:/projects/EMSE6900/src/configuration.txt'
config.read(configFilePath)

logging.basicConfig(filename='myapp.log', level=logging.DEBUG)

mydb = database.db('basquiat')
df = mydb.query(experiment_id='1693087408')

print(df)

#df['model_embedding_cos'] = df['model_embedding'].apply(lambda x: np.dot(x, df['question_embedding_'][0]) / (np.linalg.norm(x) * np.linalg.norm(df['question_embedding'][0])))
#df['question_embedding_cos'] = df['question_embedding'].apply(lambda x: np.dot(x, df['model_embedding'][0]) / (np.linalg.norm(x) * np.linalg.norm(df['model_embedding'][0])))

plotdf = df[['model_embedding_cos', 'question_embedding_cos', 'is_duplicate']].copy()
plotdf = plotdf.abs()

#plotdf = plotdf[plotdf["team"].str.contains("Team 1") == False]

#fg = sns.FacetGrid(data=plotdf, hue='is_duplicate', hue_order=[0,1], aspect=1.61)
#fg.map(plt.scatter, 'model_embedding_cos', 'question_embedding_cos').add_legend()
# plt.show(g)

g = sns.lmplot(
    x="model_embedding_cos", 
    y="question_embedding_cos", 
    hue="is_duplicate", 
    data=plotdf,  
    legend=True
)
g.set_axis_labels("Q1/Q2 Model Response Embedding Cosine Similarity", "Q1/Q2 Embedding Cosine Similarity")
plt.show()



