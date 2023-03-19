# https://huggingface.co/blog/getting-started-with-embeddings
# Closed Generative QA: In this case, no context is provided. The answer is completely generated by a model.
# https://huggingface.co/google/t5-11b-ssm-tqa

from transformers import pipeline
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import pandas as pd
import pickle

infile = '/nas/projects/EMSE6900/data/questions.csv'

# read infile in to a dataframe
df = pd.read_csv(infile)

t5_qa_model = AutoModelForSeq2SeqLM.from_pretrained("google/t5-small-ssm-nq")
t5_tok = AutoTokenizer.from_pretrained("google/t5-small-ssm-nq")

print(df["question1"][24])
input_ids = t5_tok(df["question1"][24], return_tensors="pt").input_ids
gen_output = t5_qa_model.generate(input_ids)[0]

print(t5_tok.decode(gen_output, skip_special_tokens=True))

