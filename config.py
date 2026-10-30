import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///summary.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    UPLOAD_FOLDER = 'uploads'
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'docx'}
    
    # Model settings
    MODEL_NAME = os.environ.get('MODEL_NAME') or 'facebook/bart-large-cnn'
    MAX_INPUT_LENGTH = 1024
    MAX_OUTPUT_LENGTH = 150
    CHUNK_SIZE = 800
    CHUNK_OVERLAP = 100
    
    # URL fetching settings
    URL_TIMEOUT = 10
    MAX_URL_CONTENT_SIZE = 5 * 1024 * 1024
    
    # Summarization settings
    EXTRACTIVE_RATIO = 0.3
    DEFAULT_SUMMARY_RATIO = 0.3
