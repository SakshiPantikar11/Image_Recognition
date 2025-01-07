import spacy
from transformers import pipeline
from pdfminer.high_level import extract_text


import re

# Load a pre-trained SpaCy model
nlp = spacy.load('en_core_web_sm')

print("Model loaded successfully!")

# Initialize Hugging Face's Summarization pipeline
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6", from_pt=True)
7
# Function to extract text from PDF
def extract_pdf_text(pdf_file_path):
  return extract_text(pdf_file_path)


# Function to extract legal entities and terms using NER
def extract_entities(text):
    doc = nlp(text)
    entities = []
    for ent in doc.ents:
        if ent.label_ in ['ORG', 'PERSON', 'DATE', 'GPE', 'LAW']:  # Legal entities
            entities.append((ent.text, ent.label_))
    return entities


# Function to summarize the document using Hugging Face's model
def summarize_text(text):
    summary = summarizer(text, max_length=150, min_length=50, do_sample=False)
    return summary[0]['summary_text']


# Function to process legal documents
def process_legal_document(pdf_file_path):
    # Extract text from the PDF document
    document_text = extract_pdf_text(pdf_file_path)

    # Step 1: Extract legal entities using NER
    legal_entities = extract_entities(document_text)

    # Step 2: Summarize the document
    summary = summarize_text(document_text)

    return {
        'entities': legal_entities,
        'summary': summary
    }


# Test the process with a sample legal document (replace with an actual path)
legal_document_path = 'actual_file.pdf'  # Provide the path to your PDF file. Replace 'actual_file.pdf' with the actual path
result = process_legal_document(legal_document_path)

# Print the extracted entities and the summary
print("Extracted Entities:")
for entity in result['entities']:
    print(f"{entity[0]} ({entity[1]})")

print("\nSummary of Document:")
print(result['summary'])