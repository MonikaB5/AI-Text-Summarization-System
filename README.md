# AI-Based Text Summarization System

## Project Overview
An advanced web application for intelligent document summarization using both extractive (TextRank) and abstractive (BART Transformer) techniques.

## Features
- **Extractive Summarization**: TextRank algorithm for sentence ranking
- **Abstractive Summarization**: BART Transformer model from Hugging Face
- **Multi-format Support**: PDF, DOCX, TXT files and URL extraction
- **User Authentication**: Secure registration and login system
- **Summary History**: Save and manage past summaries
- **Export Options**: Copy, download as TXT
- **Analysis Dashboard**: Word counts, compression ratio, reading time
- **ROUGE Evaluation**: Compare summaries with reference text

## Installation

### Prerequisites
- Python 3.8 or higher
- pip

### Setup Steps

1. **Clone or download the project**
```bash
cd AI_Text_Summarization_System_Full_Code
```

2. **Create virtual environment**
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. **Initialize database**
```bash
python -c "from app import app; from models.database import db; app.app_context().push(); db.create_all()"
```

6. **Run the application**
```bash
python app.py
```

7. **Access the application**
Open browser and go to `http://localhost:5000`

## Default Configuration
- Secret key: Change in production
- Database: SQLite (instance/summary.db)
- Model: facebook/bart-large-cnn (downloads on first use)

## Usage

1. Register a new account or login
2. Go to Summarize page
3. Input text, upload file (PDF/DOCX/TXT), or provide URL
4. Select summarization method and length
5. Generate summary and view analysis
6. Save to history for future reference

## Testing
```bash
pytest tests/
```

## Notes
- First run with abstractive summarization will download the BART model (~1.6GB)
- CPU inference is supported but may be slower
- For large documents, hierarchical chunking is used
- Scanned PDFs require OCR (not configured)

## Limitations
- ROUGE evaluation requires reference summary
- URL extraction respects security restrictions
- Model limited by tokenizer constraints
- No OCR for scanned documents

## Project Structure
See project files for detailed structure.
