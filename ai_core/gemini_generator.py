"""Gemini integration: builds the prompt and calls the model."""
import google.generativeai as genai

from config import GEMINI_API_KEY, GEMINI_MODEL


class GeminiDocumentGenerator:
    def __init__(self, model_name: str = GEMINI_MODEL):
        if not GEMINI_API_KEY:
            raise RuntimeError("GEMINI_API_KEY is missing. Add it to your .env file.")
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel(model_name)

    def generate_document(self, document_type, parties, terms, dates):
        prompt = (
            f"Generate a comprehensive legal document titled '{document_type}'.\n"
            f"Involved parties: {parties}\n"
            f"Effective Date: {dates}\n"
            f"Terms and conditions (semicolon separated): {terms}\n"
            "Ensure formal legal structure with numbered sections and legal clauses "
            "(recitals, definitions, obligations, term and termination, confidentiality, "
            "governing law, severability, entire agreement) and a signature block. "
            "Use plain text with section headings on their own line. "
            "Do not use markdown tables or code fences."
        )
        response = self.model.generate_content(prompt)
        return response.text
