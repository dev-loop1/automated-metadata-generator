import spacy
from transformers import pipeline
import yake

# This is our sample text for testing the NLP functions.
sample_text = """
Apple Inc. announced on Tuesday that it will be opening a new research and development center in Paris, France. 
The new facility, scheduled to open in 2026, will focus on artificial intelligence and machine learning technologies. 
CEO Tim Cook stated that this investment of over $1 billion underscores Apple's commitment to European innovation. 
Dr. Elena Petrova, a leading AI researcher from Stanford University, will head the new center. The project is expected to create over 500 new jobs in the region.
"""

# --- 2. Text Summarization ---
# We test the Hugging Face `transformers` pipeline for summarization.
print("--- TESTING SUMMARIZATION ---")
try:
    summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
    summary = summarizer(sample_text, max_length=60, min_length=10, do_sample=False)
    print("SUCCESS: Summary Generated.")
    print(summary[0]['summary_text'])
except Exception as e:
    print(f"FAILED: Could not generate summary. Error: {e}")

print("\n" + "="*50 + "\n")

# --- 3. Keyword Extraction ---
print("--- TESTING KEYWORD EXTRACTION ---")
try:
    kw_extractor = yake.KeywordExtractor()
    keywords = kw_extractor.extract_keywords(sample_text)
    print("SUCCESS: Keywords Extracted.")
    for kw, score in keywords:
        print(f"Keyword: \"{kw}\" (Score: {score:.4f})")
except Exception as e:
    print(f"FAILED: Could not extract keywords. Error: {e}")

print("\n" + "="*50 + "\n")

# --- 4. Named Entity Recognition (NER) ---
# Using `spaCy` to find and categorize entities like people, organizations, etc.
print("--- TESTING NAMED ENTITY RECOGNITION ---")
try:
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(sample_text)
    print("SUCCESS: Named Entities Found.")
    for ent in doc.ents:
        print(f"Entity: \"{ent.text}\" | Type: \"{ent.label_}\"")
except Exception as e:
    print(f"FAILED: Could not perform NER. Error: {e}")

