import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'fallback-secret-key')
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', '')
    GROQ_API_KEY = os.environ.get('GROQ_API_KEY', '')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///sop_builder.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False