import spacy
import yake
import json
import requests 

# --- Model and Pipeline Initialization ---
try:
    # Load the small English model for spaCy for Named Entity Recognition.
    nlp = spacy.load("en_core_web_sm")
except Exception as e:
    print(f"Error loading spaCy model: {e}")
    nlp = None

# YAKE keyword extractor.
kw_extractor = yake.KeywordExtractor()


def summarize_text_with_llm(text):
    if not text:
        return "No text provided to summarize."

    truncated_text = text[:8000]

    # --- Prompt to get summary of the file ---
    prompt = (
        "Your task is to act as a document analyst. Read the following text and provide a structured summary in the exact format specified below. Do not add any extra commentary.\n\n"
        "**FORMAT REQUIRED:**\n"
        "**Title:** [A concise, descriptive title for the document]\n"
        "**Overview:** [A single sentence that summarizes the main purpose or conclusion of the text]\n\n"
        "**Key Sections:**\n"
        "- Identify all the key sections of the file\n"
        "---BEGIN DOCUMENT TEXT---\n"
        f"{truncated_text}\n"
        "---END DOCUMENT TEXT---\n\n"
        "Now, generate the structured summary."
    )

    try:
        chat_history = [{"role": "user", "parts": [{"text": prompt}]}]
        payload = {"contents": chat_history}

        api_key = "AIzaSyCSOwChGIOGo0k6OismCWhrGM3LAMucvmc"
        
        if api_key == "null":
            return "ERROR: API Key not provided."

        api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"

        
        response = requests.post(api_url, json=payload)
        response.raise_for_status()
        
        result = response.json()

        if result.get("candidates") and result["candidates"][0].get("content", {}).get("parts"):
            summary = result["candidates"][0]["content"]["parts"][0]["text"]
            return summary.strip()
        else:
            
            print("LLM API Error: Unexpected response structure", result)
            return "Could not generate summary due to an API error."

    except requests.exceptions.RequestException as e:
        print(f"Error calling LLM API: {e}")
        return "Failed to generate summary. Could not connect to the summarization service."
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return "An unexpected error occurred during summarization."


def extract_keywords(text):
    if not text:
        return []
    try:
        keywords = kw_extractor.extract_keywords(text)
        return [kw[0] for kw in keywords]
    except Exception as e:
        print(f"Error during keyword extraction: {e}")
        return []


def extract_named_entities(text):

    if not nlp or not text:
        return {"Error": "NER model not available or no text provided."}

    try:
        limit = nlp.max_length
        if len(text) > limit:
            text = text[:limit]

        doc = nlp(text)
        entities = {}
        for ent in doc.ents:
            label = ent.label_
            ent_text = ent.text.strip()
            if ent_text:
                if label not in entities:
                    entities[label] = []
                if ent_text not in entities[label]:
                    entities[label].append(ent_text)
        return entities
    except Exception as e:
        print(f"Error during named entity recognition: {e}")
        return {}
