"""Central configuration for LegalEase."""
import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# Google now requires a newer flash model for new accounts.
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
API_URL = os.getenv("API_URL", "http://localhost:8000")

LOGO_PATH = os.path.join(BASE_DIR, "Image", "Logo.png")            # light bg (DOCX / PDF)
WEB_LOGO_PATH = os.path.join(BASE_DIR, "Image", "inverseLogo.png")  # dark bg (Streamlit UI)
FOOTER_TEXT = "LegalEase Inc. | contact@legalease.com | All Rights Reserved."
