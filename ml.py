import pandas as pd
from transformers import BertTokenizer, BertForSequenceClassification, Trainer, TrainingArguments
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
import torch

# Setam device-ul la GPU daca este disponibil, altfel folosim CPU
device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')

# Incarcam seturile de date din iCloud Drive
true_news = pd.read_csv('/Users/nasteapopova/Desktop/AI-in-actiune/True.csv')
fake_news = pd.read_csv('/Users/nasteapopova/Desktop/AI-in-actiune/Fake.csv')

# Adaugam etichete
true_news['label'] = 1
fake_news['label'] = 0

# Combinam seturile de date
news_dataset = pd.concat([true_news, fake_news], ignore_index=True)

# Preprocesam setul de date pentru a pastra doar 'text' si 'label'
news_dataset = news_dataset[['text', 'label']]

# Luam doar jumatate din setul de date
news_dataset = news_dataset.sample(frac=0.5, random_state=42)  # 50% din date

# Impartim setul de date in seturi de antrenament si validare
train_texts, val_texts, train_labels, val_labels = train_test_split(
    news_dataset['text'].tolist(), news_dataset['label'].tolist(), test_size=0.2, random_state=42
)

# Incarcam tokenizer-ul BERT
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

# Tokenizam textele
train_encodings = tokenizer(train_texts, truncation=True, padding=True, max_length=512)
val_encodings = tokenizer(val_texts, truncation=True, padding=True, max_length=512)

# Cream o clasa personalizata pentru dataset
class NewsDataset(torch.utils.data.Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item['labels'] = torch.tensor(self.labels[idx])
        return item

    def __len__(self):
        return len(self.labels)

# Pregatim seturile de date
train_dataset = NewsDataset(train_encodings, train_labels)
val_dataset = NewsDataset(val_encodings, val_labels)

# Incarcam modelul BERT si il mutam pe device-ul corespunzator
model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=2)
model.to(device)

# Setam argumentele pentru antrenament
training_args = TrainingArguments(
    output_dir='./results',  # Directorul pentru salvarea modelelor
    num_train_epochs=3,  # Numarul de epoci
    per_device_train_batch_size=4,  # Batch size pentru antrenament
    per_device_eval_batch_size=8,  # Batch size pentru evaluare
    warmup_steps=500,  # Numarul de pasi pentru warmup
    weight_decay=0.01,  # Valoarea pentru weight decay
    logging_dir='./logs',  # Directorul pentru loguri
    evaluation_strategy="epoch",  # Evaluam dupa fiecare epoca
    save_strategy="epoch",  # Salvam modelul dupa fiecare epoca
    load_best_model_at_end=True,  # Incarcam cel mai bun model la finalul antrenamentului
)

# Functie pentru calcularea metricei de evaluare
def compute_metrics(pred):
    labels = pred.label_ids
    preds = pred.predictions.argmax(-1)
    accuracy = accuracy_score(labels, preds)
    precision, recall, f1, _ = precision_recall_fscore_support(labels, preds, average='binary')
    return {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1': f1
    }

# Cream trainer-ul
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
    compute_metrics=compute_metrics  # Adaugam metrica de evaluare
)

# Antrenam modelul
trainer.train()

# Evaluam modelul si afisam metricele in consola
evaluation_results = trainer.evaluate()
print("Rezultatele evaluarii:", evaluation_results)

# Salvam modelul si tokenizer-ul
model.save_pretrained('./saved_model')
tokenizer.save_pretrained('./saved_model')
