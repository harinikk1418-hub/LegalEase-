from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from ai_core.gemini_generator import GeminiDocumentGenerator

router = APIRouter()
_generator = None


def get_generator() -> GeminiDocumentGenerator:
    """Lazy init so the API can start (and show a clear error) without a key."""
    global _generator
    if _generator is None:
        _generator = GeminiDocumentGenerator()
    return _generator


class DocumentRequest(BaseModel):
    document_type: str = Field(..., min_length=2)
    parties: str = Field(..., min_length=2)
    terms: str = ""
    dates: str = ""


@router.post("/generate")
def generate_legal_document(request: DocumentRequest):
    try:
        response = get_generator().generate_document(
            request.document_type, request.parties, request.terms, request.dates
        )
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc))
    except Exception as exc:  # Gemini/network errors
        raise HTTPException(status_code=502, detail=f"AI generation failed: {exc}")
    return {"document": response}
