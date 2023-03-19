#https://www.sbert.net/examples/training/quora_duplicate_questions/README.html

from sentence_transformers import SentenceTransformer
model = SentenceTransformer('model_name')

train_samples = []
with open(os.path.join(dataset_path, "classification/train_pairs.tsv"), encoding='utf8') as fIn:
    reader = csv.DictReader(fIn, delimiter='\t', quoting=csv.QUOTE_NONE)
    for row in reader:
        sample = InputExample(texts=[row['question1'], row['question2']], label=int(row['is_duplicate']))
        train_samples.append(sample)


train_dataset = SentencesDataset(train_samples, model=model)
train_dataloader = DataLoader(train_dataset, shuffle=True, batch_size=train_batch_size)
train_loss = losses.OnlineContrastiveLoss(model=model, distance_metric=distance_metric, margin=margin)

