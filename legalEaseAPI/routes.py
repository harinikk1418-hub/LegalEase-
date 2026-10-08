from fastapi import APIRouter, HTTPException
from google.genai.errors import ServerError
from pydantic import BaseModel, Field

from ai_core.gemini_generator import GeminiDocumentGenerator

router = APIRouter()
_generator = None  # created lazily so the server can start even before the key is set


def get_generator() -> GeminiDocumentGenerator:
    global _generator
    if _generator is None:
        _generator = GeminiDocumentGenerator()
    return _generator


class DocumentRequest(BaseModel):
    document_type: str = Field(..., min_length=2, max_length=200)
    parties: str = Field(..., min_length=2, max_length=2000)
    terms: str = Field("", max_length=8000)
    dates: str = Field(..., min_length=2, max_length=100)


@router.post("/generate")
def generate_legal_document(request: DocumentRequest):
    try:
        text = get_generator().generate_document(
            request.document_type, request.parties, request.terms, request.dates
        )
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except ServerError as e:
        if e.code in {500, 502, 503, 504}:
            raise HTTPException(
                status_code=503,
                detail="Gemini is temporarily unavailable. Please try again shortly.",
                headers={"Retry-After": "5"},
            ) from e
        raise HTTPException(status_code=502, detail=f"Gemini error: {e}") from e
    except Exception as e:  # network / quota / API errors
        raise HTTPException(status_code=502, detail=f"Gemini error: {e}")
    return {"document": text}
