import pandas as pd
from transformers import BertTokenizer, BertForSequenceClassification, Trainer, TrainingArguments
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
import torch
import re
import os

# Set the device
device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')

# Define model save path
model_dir = './saved_model'

# Load datasets
true_news = pd.read_csv('/Users/nasteapopova/Desktop/AI-in-actiune/True.csv')
fake_news = pd.read_csv('/Users/nasteapopova/Desktop/AI-in-actiune/Fake.csv')

# Add labels
true_news['label'] = 1
fake_news['label'] = 0

# Combine datasets
news_dataset = pd.concat([true_news, fake_news], ignore_index=True)

# Preprocess the dataset
news_dataset = news_dataset[['text', 'label']]
news_dataset = news_dataset.sample(frac=0.2, random_state=42)  # Use 20% of the dataset

# Split the dataset
train_texts, val_texts, train_labels, val_labels = train_test_split(
    news_dataset['text'].tolist(), news_dataset['label'].tolist(), test_size=0.2, random_state=42
)

# Load the tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

# Clean text function
def clean_text(text):
    text = re.sub(r'\s+', ' ', text)  # Remove extra whitespace
    text = text.strip()  # Remove leading/trailing spaces
    return text

# Clean the training and validation texts
train_texts = [clean_text(text) for text in train_texts]
val_texts = [clean_text(text) for text in val_texts]

# Tokenize the texts
train_encodings = tokenizer(train_texts, truncation=True, padding=True, max_length=128)
val_encodings = tokenizer(val_texts, truncation=True, padding=True, max_length=128)

# Create a custom dataset class
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

# Prepare datasets
train_dataset = NewsDataset(train_encodings, train_labels)
val_dataset = NewsDataset(val_encodings, val_labels)

# Load the model and move to the device if already trained
if os.path.exists(model_dir):
    print("Modelul antrenat a fost gasit. Se incarca modelul salvat...")
    model = BertForSequenceClassification.from_pretrained(model_dir)
else:
    print("Modelul antrenat nu a fost gasit. Incepem antrenarea...")
    model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=2)
    model.to(device)

    # Set training arguments
    training_args = TrainingArguments(
        output_dir='./results',
        num_train_epochs=3,  # Increased epochs for better training
        per_device_train_batch_size=4,  # Adjusted batch size for better performance
        per_device_eval_batch_size=8,
        warmup_steps=500,
        weight_decay=0.01,
        logging_dir='./logs',
        evaluation_strategy="epoch",
        save_strategy="epoch",
        load_best_model_at_end=True,
    )

    # Define evaluation metrics
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

    # Create the Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
        compute_metrics=compute_metrics
    )

    # Train the model
    trainer.train()

    # Evaluate the model
    evaluation_results = trainer.evaluate()
    print("Evaluation Results:", evaluation_results)

    # Save the model and tokenizer
    model.save_pretrained(model_dir)
    tokenizer.save_pretrained(model_dir)

# Prediction function
def predict_news(news_text):
    model_for_prediction = model.to('cpu')
    inputs = tokenizer(clean_text(news_text), truncation=True, padding=True, max_length=128, return_tensors="pt")
    inputs = {key: val.to('cpu') for key, val in inputs.items()}
    
    with torch.no_grad():
        outputs = model_for_prediction(**inputs)
    
    prediction = torch.argmax(outputs.logits, dim=1).item()
    return "True" if prediction == 1 else "False"

# Example usage
news_example = input("Enter the news article text for verification: ")
result = predict_news(news_example)
print(f"Prediction for the news article: {result}")
