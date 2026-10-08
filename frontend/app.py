import os
import sys

import requests
import streamlit as st

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import BACKEND_URL, LOGO_PATH  # noqa: E402
from frontend.formatters import (  # noqa: E402
    format_docx, format_html_preview, format_pdf, sanitize_text,
)

st.set_page_config(
    page_title="LegalEase | Document drafting",
    page_icon=":material/balance:",
    layout="wide",
)

if "generated_text" not in st.session_state:
    st.session_state.generated_text = ""
if "show_edit" not in st.session_state:
    st.session_state.show_edit = False

with st.container(horizontal=True, vertical_alignment="center"):
    if os.path.exists(LOGO_PATH):
        st.image(LOGO_PATH, width=190)
    st.badge("AI-assisted drafting", icon=":material/auto_awesome:", color="green")

st.title("Build a stronger first draft", icon=":material/description:")
st.caption(
    "Turn the key details of your agreement into a clear, editable legal document."
)

form_column, guide_column = st.columns([1.65, 0.85], gap="large")

with form_column:
    with st.container(border=True):
        st.subheader("Document details", icon=":material/edit_document:")
        st.caption("Add the essentials. You can review and edit the draft before downloading.")

        with st.form("document_form", clear_on_submit=False):
            type_column, date_column = st.columns(2)
            with type_column:
                document_type = st.text_input(
                    "Document type",
                    placeholder="e.g. Service agreement, NDA",
                )
            with date_column:
                dates = st.text_input(
                    "Effective date",
                    placeholder="e.g. 1 October 2026",
                )
            parties = st.text_area(
                "Parties involved",
                placeholder="Names of the people or organizations entering the agreement",
                height=110,
            )
            terms = st.text_area(
                "Key terms and conditions",
                placeholder="Add the main obligations, payment terms, deadlines, and other details. Separate terms with semicolons.",
                height=150,
            )
            submitted = st.form_submit_button(
                "Generate document",
                type="primary",
                icon=":material/auto_awesome:",
                width="stretch",
            )

    if submitted:
        if not (document_type.strip() and parties.strip() and dates.strip()):
            st.warning(
                "Please add the document type, parties involved, and effective date."
            )
        else:
            with st.spinner("Preparing your first draft..."):
                try:
                    response = requests.post(
                        f"{BACKEND_URL}/generate",
                        json={
                            "document_type": document_type,
                            "parties": parties,
                            "terms": terms,
                            "dates": dates,
                        },
                        timeout=180,
                    )
                    if response.status_code == 200:
                        payload = response.json()
                        document = payload.get("document")
                        if not isinstance(document, str) or not document.strip():
                            st.error("The backend returned an empty document.")
                        else:
                            st.session_state.generated_text = sanitize_text(document)
                            st.session_state.doc_type = document_type
                            st.session_state.terms = terms
                            st.session_state.show_edit = False
                            st.success("Your first draft is ready to review.")
                    else:
                        if response.status_code == 503:
                            st.warning(
                                "Gemini is temporarily unavailable. Please try again "
                                "in a few seconds; your details are still here."
                            )
                        else:
                            try:
                                detail = response.json().get("detail", response.text)
                            except ValueError:
                                detail = response.text
                            st.error(f"Backend error {response.status_code}: {detail}")
                except requests.exceptions.RequestException as error:
                    st.error(
                        f"Could not reach the backend at {BACKEND_URL}. "
                        f"Check that the API is running. ({error})"
                    )
                except (ValueError, TypeError) as error:
                    st.error(f"The backend returned an invalid response: {error}")

with guide_column:
    with st.container(border=True):
        st.subheader("A simple workflow", icon=":material/steps:")
        st.markdown(
            """
            **1. Share the essentials**  
            Add the parties, date, and main terms.

            **2. Review your draft**  
            Edit the generated text to suit your needs.

            **3. Export when ready**  
            Download as TXT, DOCX, or PDF.
            """
        )
    st.caption(
        "LegalEase creates a starting point, not legal advice. "
        "Ask a qualified lawyer to review documents before signing."
    )

if st.session_state.generated_text:
    st.space("large")
    st.header("Your document", icon=":material/description:")
    st.caption("Review the draft carefully. Your edits are included in every download.")

    with st.container(border=True):
        if st.session_state.show_edit:
            st.text_area(
                "Edit document",
                key="generated_text",
                height=420,
            )
        else:
            st.markdown(
                format_html_preview(st.session_state.generated_text),
                unsafe_allow_html=True,
            )

        if st.button(
            "Finish editing" if st.session_state.show_edit else "Edit document",
            icon=(
                ":material/check:"
                if st.session_state.show_edit
                else ":material/edit:"
            ),
        ):
            st.session_state.show_edit = not st.session_state.show_edit
            st.rerun()

    text = st.session_state.generated_text
    document_type = st.session_state.get("doc_type", "Legal Document")
    terms = st.session_state.get("terms", "")
    filename = document_type.strip().replace(" ", "_").lower() or "legal_document"

    st.subheader("Download your draft", icon=":material/download:")
    txt_column, docx_column, pdf_column = st.columns(3)
    with txt_column:
        st.download_button(
            "Download TXT",
            data=text,
            file_name=f"{filename}.txt",
            mime="text/plain",
            icon=":material/description:",
            width="stretch",
        )
    with docx_column:
        st.download_button(
            "Download DOCX",
            data=format_docx(text, document_type, terms),
            file_name=f"{filename}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            icon=":material/article:",
            width="stretch",
        )
    with pdf_column:
        st.download_button(
            "Download PDF",
            data=format_pdf(text, document_type, terms),
            file_name=f"{filename}.pdf",
            mime="application/pdf",
            icon=":material/picture_as_pdf:",
            width="stretch",
        )
