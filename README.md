# LegalEase - AI Legal Document Generator
FastAPI backend + Streamlit frontend + Google Gemini. Exports TXT / DOCX / PDF.

## Structure
```
LegalEase/
├── ai_core/gemini_generator.py   # Gemini prompt + call
├── legalEaseAPI/main.py, routes.py   # FastAPI (/, /health, POST /generate)
├── frontend/app.py, formatters.py    # Streamlit UI + docx/pdf/html export
├── Image/Logo.png, inverseLogo.png   # replace with your own logo
├── config.py  .env  requirements.txt  render.yaml  run.sh  run.bat
```

## Run locally in VS Code
1. Open the folder in VS Code (File > Open Folder). Python 3.10+ required.
2. Terminal:
   ```
   python -m venv venv
   venv\Scripts\activate          (Mac/Linux: source venv/bin/activate)
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and put your Gemini API key (https://aistudio.google.com/apikey).
4. Start (two terminals):
   ```
   uvicorn legalEaseAPI.main:app --reload
   streamlit run frontend/app.py
   ```
   Or just run `run.bat` (Windows) / `./run.sh` (Mac/Linux).
5. Open http://localhost:8501

## Deploy on Render
1. Push this folder to a GitHub repo (`.env` is git-ignored, never commit your key).
2. Render dashboard > New > **Blueprint** > pick the repo (it reads `render.yaml`).
3. Set `GEMINI_API_KEY` on **legalease-api**. Deploy it, copy its URL (https://legalease-api.onrender.com).
4. Set `BACKEND_URL` on **legalease-web** to that URL and deploy.
5. Open the legalease-web URL. (Free plan sleeps when idle: first request can take ~50 s.)

Manual alternative (no blueprint): create two Web Services with the build/start commands from `render.yaml`.
