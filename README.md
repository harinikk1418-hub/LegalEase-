# LegalEase: AI-Powered Legal Document Generator
Streamlit frontend + FastAPI backend + Google Gemini.

## Run
```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env            # put your GEMINI_API_KEY inside
./run.sh                        # Windows: run.bat
```
Backend: http://localhost:8000/docs  |  Website: http://localhost:8501

Manual start: `uvicorn legalEaseAPI.main:app --reload` then `streamlit run frontend/app.py`.

## Docker
`docker compose up --build`

## Structure
```
ai_core/         gemini_generator.py, generator.py (DOCX/PDF/HTML formatting)
legalEaseAPI/    main.py, routes.py
frontend/        app.py (Streamlit)
Image/           Logo.png, inverseLogo.png (replace with your own)
tests/           pytest formatter tests
```
Note: Google has moved to newer flash models for recent accounts; the current default is `gemini-3.8-flash` (change `GEMINI_MODEL` in `.env` if needed).
Generated documents are drafts, not legal advice - have a lawyer review them.
