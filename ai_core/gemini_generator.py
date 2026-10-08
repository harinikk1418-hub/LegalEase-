"""Gemini integration: builds a structured prompt and returns the legal text."""
import logging
import time

from google import genai
from google.genai import errors, types

from config import GEMINI_API_KEY, GEMINI_MODEL

logger = logging.getLogger(__name__)
_RETRY_DELAYS_SECONDS = (1, 2)
_RETRYABLE_STATUS_CODES = {500, 502, 503, 504}
_REQUEST_TIMEOUT_MS = 45_000

SYSTEM_INSTRUCTION = (
    "You are a careful legal drafting assistant. You write formal, well-structured "
    "legal documents in plain text only. Do NOT use markdown symbols such as #, ** or *. "
    "Number each main section like '1. Services:' on its own line. Use '-' for bullet "
    "points. Where information is missing, use clear placeholders in [square brackets]. "
    "Always end with a signature block for every party."
)


class GeminiDocumentGenerator:
    def __init__(self, model_name=None):
        if not GEMINI_API_KEY:
            raise RuntimeError("GEMINI_API_KEY is not set. Add it to .env or Render environment.")
        self.client = genai.Client(
            api_key=GEMINI_API_KEY,
            http_options=types.HttpOptions(
                timeout=_REQUEST_TIMEOUT_MS,
                retry_options=types.HttpRetryOptions(attempts=1),
            ),
        )
        self.model_name = model_name or GEMINI_MODEL

    def generate_document(self, document_type, parties, terms, dates):
        term_lines = [t.strip() for t in terms.split(";") if t.strip()]
        terms_block = "\n".join(f"- {t}" for t in term_lines) or "- (none provided)"

        prompt = (
            f"Generate a comprehensive legal document titled '{document_type}'.\n"
            f"Involved parties: {parties}\n"
            f"Effective date: {dates}\n"
            f"Terms and conditions that MUST be included and expanded into formal clauses:\n"
            f"{terms_block}\n\n"
            "Ensure a formal legal structure with a title, preamble/recitals, multiple numbered "
            "sections and legal clauses (definitions, obligations, payment/consideration where "
            "relevant, confidentiality, termination, governing law, dispute resolution, "
            "severability, entire agreement) and a signature block."
        )

        for attempt in range(len(_RETRY_DELAYS_SECONDS) + 1):
            try:
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_INSTRUCTION,
                        temperature=0.4,
                    ),
                )
                break
            except errors.ServerError as error:
                if (
                    error.code not in _RETRYABLE_STATUS_CODES
                    or attempt == len(_RETRY_DELAYS_SECONDS)
                ):
                    raise
                delay = _RETRY_DELAYS_SECONDS[attempt]
                logger.warning(
                    "Gemini returned a transient server error; retrying in %s seconds "
                    "(attempt %s of %s).",
                    delay,
                    attempt + 1,
                    len(_RETRY_DELAYS_SECONDS) + 1,
                )
                time.sleep(delay)

        if not response.text:
            raise RuntimeError("Gemini returned an empty response. Try rephrasing your input.")
        return response.text
