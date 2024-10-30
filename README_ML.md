This is a README file dedicated to the Machine Learning part.

Title: Fake News Detection with BERT

This project focuses on using machine learning techniques, specifically the BERT model, to differentiate fake news from real news. Leveraging advanced natural language processing, the code classifies news articles based on a dataset containing labeled articles, enabling predictions of whether an article is likely true or false.

The dataset consists of two CSV files: one for true news articles and another for fake news articles. For efficiency, a 40% sample of the dataset is used, labeling each article with 1 for true and 0 for fake.

The BERT model is pre-trained using the Hugging Face Transformers library, which provides easy access to pre-trained models for text classification tasks. BERT’s architecture includes attention mechanisms that help the model understand the context around each word, making it effective in distinguishing between real and fake news.

The code includes several preprocessing steps. First, it cleans the text data by removing extraneous whitespace and irrelevant characters. It then tokenizes the text into smaller units (tokens) that BERT can process. A custom dataset class is implemented to format the data for training with PyTorch, enabling it to be loaded through a DataLoader. The data is split into training and validation sets to assess the model’s performance, tracking metrics like accuracy, precision, recall, and F1 score.

If a trained model already exists in the specified directory, the code loads it instead of training a new one, saving time and resources. It can also detect if a GPU is available, allowing for faster processing.

Once trained, the model can predict new news articles. Users can input text, and the model will analyze it, outputting whether the article is predicted to be true or false. This feature offers quick, real-time predictions.

Overall, this project combines data processing, model training, and evaluation to provide a robust solution for fake news detection. It demonstrates the power of BERT and the flexibility of Hugging Face Transformers in addressing real-world challenges in natural language processing.