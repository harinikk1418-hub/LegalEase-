import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests
import streamlit as st

from ai_core.generator import (
    format_docx, format_html_preview, format_pdf, sanitize_text,
)
from config import API_URL, WEB_LOGO_PATH

st.set_page_config(page_title="LegalEase", page_icon="⚖️", layout="wide")

st.markdown(
    """
    <style>
        :root {
            --bg: #f5f7fb;
            --panel: rgba(255, 255, 255, 0.9);
            --panel-strong: #ffffff;
            --primary: #1e3a5f;
            --primary-soft: #eaf2ff;
            --accent: #d4af6a;
            --text: #1e2430;
            --muted: #58657a;
            --border: rgba(30, 58, 95, 0.12);
            --success: #1f8a5c;
        }

        .stApp {
            background: linear-gradient(180deg, #eef4ff 0%, #f7f8fb 100%);
        }

        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            max-width: 1180px;
        }

        .hero-card {
            background: linear-gradient(135deg, #102a43 0%, #1f456d 55%, #2a5a8a 100%);
            border-radius: 22px;
            padding: 2rem 2.3rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 18px 45px rgba(16, 42, 67, 0.18);
        }

        .hero-card h1 {
            color: white;
            margin: 0;
            font-size: 2.3rem;
            font-weight: 700;
            letter-spacing: -0.04em;
        }

        .hero-card p {
            color: rgba(255, 255, 255, 0.8);
            margin-top: 0.6rem;
            margin-bottom: 0;
            font-size: 1.02rem;
        }

        .form-card {
            background: rgba(255, 255, 255, 0.82);
            border: 1px solid var(--border);
            border-radius: 18px;
            padding: 1.5rem;
            box-shadow: 0 10px 30px rgba(15, 23, 42, 0.05);
        }

        .result-card {
            background: #f8fafc;
            border: 1px solid var(--border);
            border-radius: 18px;
            padding: 1rem 1.05rem;
            margin-top: 1.25rem;
            box-shadow: inset 0 1px 0 rgba(255,255,255,0.9);
        }

        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea {
            border-radius: 12px !important;
            border: 1px solid rgba(30, 58, 95, 0.15) !important;
            background: #ffffff !important;
            color: var(--text) !important;
            box-shadow: none !important;
        }

        .stTextInput > div > div > input:focus,
        .stTextArea > div > div > textarea:focus {
            border-color: rgba(30, 58, 95, 0.55) !important;
            box-shadow: 0 0 0 1px rgba(30, 58, 95, 0.15) !important;
        }

        .stButton > button {
            border-radius: 12px !important;
            font-weight: 600 !important;
            padding: 0.7rem 1.2rem !important;
            background: linear-gradient(135deg, #1d3557 0%, #2b4d7a 100%) !important;
            color: white !important;
            border: none !important;
            box-shadow: 0 8px 24px rgba(29, 53, 87, 0.2) !important;
        }

        .stDownloadButton > button {
            border-radius: 12px !important;
            background: #eef4ff !important;
            color: var(--primary) !important;
            border: 1px solid rgba(30, 58, 95, 0.15) !important;
            font-weight: 600 !important;
        }

        div[data-testid="stNotification"] {
            background: rgba(255,255,255,0.9);
            border: 1px solid var(--border);
        }
    </style>
    """,
    unsafe_allow_html=True,
)

for key, default in {"generated_text": "", "show_edit": False, "meta": {}}.items():
    st.session_state.setdefault(key, default)

_, col2, _ = st.columns([1, 2, 1])
with col2:
    if os.path.exists(WEB_LOGO_PATH):
        st.image(WEB_LOGO_PATH, use_container_width=True)
    else:
        st.markdown("<h1 style='text-align:center;color:#1e3a5f'>⚖️ LegalEase</h1>", unsafe_allow_html=True)

st.markdown(
    """
    <div class="hero-card">
        <h1>AI Legal Document Generator</h1>
        <p>Draft clear, professional legal documents in minutes with guided inputs and export-ready output.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.container():
    st.markdown('<div class="form-card">', unsafe_allow_html=True)
    col1, col2 = st.columns([1.3, 1])
    with col1:
        document_type = st.text_input("Document Type", placeholder="Agreement, Contract, NDA, etc.")
    with col2:
        dates = st.text_input("Effective Date", placeholder="DD/MM/YYYY or month/year")

    parties = st.text_area("Parties Involved", placeholder="Example: Acme Corp. and BrightPath Solutions Ltd.")
    terms = st.text_area("Terms & Conditions", placeholder="Add key clauses; use semicolons for bullet points.")

    button_col, _ = st.columns([1, 4])
    with button_col:
        if st.button("Generate Document", type="primary"):
            if not document_type.strip() or not parties.strip():
                st.warning("Please enter at least the document type and the parties involved.")
            else:
                with st.spinner("Drafting your document..."):
                    try:
                        resp = requests.post(
                            f"{API_URL}/generate",
                            json={"document_type": document_type, "parties": parties,
                                  "terms": terms, "dates": dates},
                            timeout=180,
                        )
                        resp.raise_for_status()
                        st.session_state.generated_text = sanitize_text(resp.json()["document"])
                        st.session_state.meta = {"type": document_type, "terms": terms}
                        st.session_state.show_edit = False
                        st.success("✅ Document Generated Successfully!")
                    except requests.HTTPError:
                        detail = resp.json().get("detail", resp.text) if resp.content else resp.status_code
                        st.error(f"Backend error: {detail}")
                    except requests.RequestException as exc:
                        st.error(f"Cannot reach the backend at {API_URL}. Is it running? ({exc})")
    st.markdown('</div>', unsafe_allow_html=True)

text = st.session_state.generated_text
if text:
    st.markdown('<div class="result-card">', unsafe_allow_html=True)
    styled = format_html_preview(text)
    st.markdown(
        "<div style='background:#0f1626;color:#e6e9ef;padding:18px;border-radius:12px;"
        f"max-height:420px;overflow-y:auto;border:1px solid rgba(255,255,255,0.08)'>{styled}</div>",
        unsafe_allow_html=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("✏️ Edit Document"):
        st.session_state.show_edit = not st.session_state.show_edit

    if st.session_state.show_edit:
        st.session_state.generated_text = st.text_area(
            "Edit Document Below:", value=st.session_state.generated_text, height=300
        )
        text = st.session_state.generated_text

    meta = st.session_state.meta
    doc_type = meta.get("type", "Legal Document")
    base = doc_type.replace(" ", "_").lower()

    dl_col1, dl_col2, dl_col3 = st.columns(3)
    with dl_col1:
        st.download_button("📄 TXT", data=text, file_name=f"{base}.txt", mime="text/plain")
    with dl_col2:
        st.download_button(
            "📝 DOCX",
            data=format_docx(text, doc_type, meta.get("terms", "")),
            file_name=f"{base}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )
    with dl_col3:
        st.download_button(
            "📕 PDF",
            data=format_pdf(text, doc_type, meta.get("terms", "")),
            file_name=f"{base}.pdf",
            mime="application/pdf",
        )
else:
    st.info("Click 'Generate Document' to start")
