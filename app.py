import streamlit as st
import io
import json
import time
import os
from dotenv import load_dotenv

# --- Step 1: Load environment variables at the very beginning ---
load_dotenv()

# --- Step 2: Import our custom modules ---
from app.file_processor import extract_text_from_pdf, extract_text_from_docx, extract_text_from_txt
from app.nlp_engine import summarize_text_with_llm, extract_keywords, extract_named_entities


# --- Step 3: Check for the API key and stop if it's missing ---
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY or API_KEY == "PASTE_YOUR_GOOGLE_AI_STUDIO_API_KEY_HERE":
    st.error("EMINI_API_KEY not found!")
    st.info("Please create a file named `.env` in the root of your project and add your Google AI Studio API key to it. For example: `GEMINI_API_KEY='your_api_key_here'`")
    st.stop() # Stop the app from running further.


# --- Page Configuration ---
st.set_page_config(
    page_title="Automated Metadata Generator",
    page_icon="🤖",
    layout="wide"
)

# --- UI Layout ---
st.title("📄 Automated Metadata Generator")
st.markdown("""
This tool analyzes your documents and automatically generates rich metadata.
- **Upload a document** (`.pdf`, `.docx`, or `.txt`).
- The system extracts the text and identifies key information using advanced AI.
- **View the results**, including a high-quality summary, keywords, and named entities.
""")

# --- File Uploader and Processing Logic ---
uploaded_file = st.file_uploader(
    "Choose a document to analyze",
    type=["pdf", "docx", "txt"],
    help="Upload a file to start the metadata generation process."
)

if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    file_stream = io.BytesIO(bytes_data)

    st.subheader("File Details")
    file_details = {
        "File Name": uploaded_file.name,
        "File Type": uploaded_file.type,
        "File Size (KB)": round(uploaded_file.size / 1024, 2)
    }
    st.json(file_details)

    with st.spinner("Analyzing document... This may take a moment."):
        start_time = time.time()
        st.write("---")
        st.write("Step 1: Extracting Text...")

        text_content = ""
        if uploaded_file.type == "application/pdf":
            text_content = extract_text_from_pdf(file_stream)
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            text_content = extract_text_from_docx(file_stream)
        elif uploaded_file.type == "text/plain":
            text_content = extract_text_from_txt(file_stream)

        if not text_content:
            st.error("Could not extract text from the document. The file might be empty, corrupted, or an image-based PDF requiring OCR.")
        else:
            st.success(f"Text extracted successfully! ({len(text_content)} characters)")
            text_extraction_time = time.time() - start_time

            st.write("Step 2: Generating Metadata...")
            nlp_start_time = time.time()

            summary = summarize_text_with_llm(text_content)
            keywords = extract_keywords(text_content)
            entities = extract_named_entities(text_content)

            nlp_processing_time = time.time() - nlp_start_time

            st.subheader("Generated Metadata")
            st.markdown("---")

            col1, col2 = st.columns(2)

            with col1:
                st.info("Summary")
                st.write(summary)

            with col2:
                st.info("🔑 Keywords")
                st.write("  ".join(f"`{kw}`" for kw in keywords))

            st.info("Named Entities")
            st.write("Entities identified in the text, such as people, organizations, and locations.")
            st.json(entities)

            final_metadata = {
                "fileInfo": file_details,
                "extractedContent": {
                    "characterCount": len(text_content),
                    "wordCount": len(text_content.split())
                },
                "generatedMetadata": {
                    "summary": summary,
                    "keywords": keywords,
                    "namedEntities": entities
                },
                "processingStats": {
                    "textExtractionTime_s": round(text_extraction_time, 2),
                    "nlpProcessingTime_s": round(nlp_processing_time, 2),
                    "totalTime_s": round(time.time() - start_time, 2)
                }
            }

            st.subheader("Complete Metadata (JSON Output)")
            st.json(final_metadata)

            st.download_button(
                label="Download Metadata as JSON",
                data=json.dumps(final_metadata, indent=4),
                file_name=f"{file_details['File Name']}_metadata.json",
                mime="application/json",
            )
