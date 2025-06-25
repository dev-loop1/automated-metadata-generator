# Automated Metadata Generator

An intelligent web application that analyzes unstructured documents (`.pdf`, `.docx`, `.txt`) to automatically generate rich, semantic metadata — including AI-powered summaries, keywords, and named entities.

---

## Project Overview

In the age of information overload, quickly finding and understanding documents is a significant challenge. This project addresses that problem by providing an automated system to enhance document discoverability, classification, and analysis.

The application uses a sophisticated pipeline: it extracts text from various document formats (including scanned PDFs via Optical Character Recognition), then applies advanced AI and NLP models to generate structured, insightful metadata.

---

## Key Features

- **Multi-Format Support**  
  Accepts and processes `.pdf`, `.docx`, and `.txt` files.

- **Optical Character Recognition (OCR)**  
  Automatically detects image-based PDFs and uses the **Tesseract** engine to extract text.

- **AI-Powered Summarization**  
  Uses the **Google Gemini 2.0 Flash API** to generate high-quality, human-like summaries and identify important sections.

- **Keyword Extraction**  
  Employs the **YAKE** (Yet Another Keyword Extractor) algorithm to identify the most relevant terms and phrases.

- **Named Entity Recognition (NER)**  
  Uses **spaCy** to extract entities such as people, organizations, locations, and dates.

- **Intuitive Web Interface**  
  Built with **Streamlit** to offer a simple, interactive way to upload documents and view metadata.

- **Downloadable Results**  
  Allows users to download the complete generated metadata as a structured `.json` file.

---

## Technology Stack

| Category                | Tools & Technologies              |
|-------------------------|-----------------------------------|
| Backend & Core Logic    | Python 3.9+                       |
| Web Framework           | Streamlit                         |
| AI Summarization        | Google Gemini 1.5 Pro API         |
| NER (Named Entity Rec.) | spaCy                             |
| Keyword Extraction      | YAKE                              |
| File Parsing            | PyMuPDF, python-docx              |
| OCR Engine              | Tesseract-OCR                     |
| Environment Management  | python-dotenv                     |

---

## Local Setup & Reproduction Guide

Follow these steps to set up and run the project on your local machine.

### 1. Prerequisites

- **Python 3.9+**  
- **Git**  
- **Tesseract-OCR Engine** (must be installed separately):

**macOS**  
  ```bash
  brew install tesseract
  ```

**Windows**  

Download the installer from the [Tesseract at UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki) page.
*Ensure the option to add Tesseract to your system's PATH is selected during installation.*

**Linux (Debian/Ubuntu)**

```bash
sudo apt update && sudo apt install tesseract-ocr
```

---

### 2. Clone the Repository

```bash
git clone https://github.com/dev-loop1/automated-metadata-generator.git
cd automated-metadata-generator
```

---

### 3. Set Up Virtual Environment & Dependencies

It is recommended to use a virtual environment.

```bash
# Create a virtual environment
python3 -m venv venv

# Activate it
# macOS/Linux:
source venv/bin/activate

# Windows:
# .\venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

---

### 4. Add Your API Key

* Get a **Google Gemini API key** from [Google AI Studio](https://makersuite.google.com/app).
* In the project root, create a `.env` file with the following content:

```
GEMINI_API_KEY="PASTE_YOUR_API_KEY_HERE"
```

> The `.gitignore` is already configured to exclude this file.

---

### 5. Run the Application

```bash
streamlit run app.py
```

This will launch the web application in your default browser. You can now upload documents and view their automatically generated metadata.

---

