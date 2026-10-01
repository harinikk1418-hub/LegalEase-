import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai_core.generator import format_docx, format_pdf, format_html_preview, sanitize_text

SAMPLE = "## NDA\n\n1. Confidentiality:\nThe \u201cParty\u201d agrees \u2014 always.\n<script>x</script>"


def test_sanitize():
    assert "\u201c" not in sanitize_text(SAMPLE)


def test_html_escapes():
    assert "<script>" not in format_html_preview(SAMPLE)


def test_docx():
    assert format_docx(SAMPLE, "NDA", "A; B")[:2] == b"PK"


def test_pdf():
    assert format_pdf(SAMPLE, "NDA", "A; B")[:4] == b"%PDF"
