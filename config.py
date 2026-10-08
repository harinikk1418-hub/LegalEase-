"""Central configuration. Values come from the .env file (local) or from
environment variables (Render)."""
import os
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"), override=True)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")

# Where the Streamlit frontend finds the FastAPI backend
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000").rstrip("/")

LOGO_PATH = os.path.join(BASE_DIR, "Image", "Logo.png")
WEB_LOGO_PATH = os.path.join(BASE_DIR, "Image", "inverseLogo.png")
FOOTER_TEXT = "LegalEase Inc. | contact@legalease.com | All Rights Reserved."
