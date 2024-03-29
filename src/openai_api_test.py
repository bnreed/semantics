# https://platform.openai.com/docs/guides/completion

import json
import os
import openai
import time
openai.organization =  os.getenv("OPENAI_API_ORG")
#openai.api_key = os.getenv("OPENAI_API_KEY")
#openai.api_base = "https://api.openai.com/v1"

openai.api_key="sk-111111111111111111111111111111111111111111111111"
openai.api_base="http://127.0.0.1:5001/v1"

models = openai.Model.list()
for model in models.data:
    print(model.id)

print('*************************')

# list engines
engines = openai.Engine.list()
for engine in engines.data:
    print(engine.id)



# text completion, get embeddings