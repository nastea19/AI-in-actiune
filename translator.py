# enter this command in the terminal
#-> pip install googletrans==4.0.0-rc1

import csv
from googletrans import Translator

# Define the input and output file paths
input_file_path = 'stiri_vizualizari1.csv'  # Change to your actual input file path
output_file_path = 'Translated.csv'  # Change to your desired output path

# Initialize the translator
translator = Translator()

# Define a function to translate text from Romanian to English
def translate_to_english(text):
    try:
        translated = translator.translate(text, src='ro', dest='en').text
        return translated
    except Exception as e:
        print(f"Translation error for text: {text}. Error: {e}")
        return text  # Return original text if translation fails

# Read the CSV file and translate the 'Titlu' and 'Rezumat' columns
with open(input_file_path, mode='r', encoding='utf-8') as input_file:
    csv_reader = csv.DictReader(input_file)  # Read CSV as a dictionary
    # Define new field names for the translated 'Titlu' and 'Rezumat'
    fieldnames = ['text_en_Titlu', 'text_en_Rezumat']

    # Open the output file
    with open(output_file_path, mode='w', newline='', encoding='utf-8') as output_file:
        csv_writer = csv.DictWriter(output_file, fieldnames=fieldnames)  # Create a CSV writer
        csv_writer.writeheader()  # Write the header row

        # Iterate through the rows in the input file
        for row in csv_reader:
            translated_row = {}
            # Translate the 'Titlu' column if it exists
            if 'Titlu' in row:
                translated_row['text_en_Titlu'] = translate_to_english(row['Titlu'])
            else:
                print("Error: 'Titlu' column not found in the row.")
                translated_row['text_en_Titlu'] = ''
            
            # Translate the 'Rezumat' column if it exists
            if 'Rezumat' in row:
                translated_row['text_en_Rezumat'] = translate_to_english(row['Rezumat'])
            else:
                print("Error: 'Rezumat' column not found in the row.")
                translated_row['text_en_Rezumat'] = ''

            csv_writer.writerow(translated_row)  # Write the translated texts to the output file

print(f"Translated file saved as {output_file_path}")