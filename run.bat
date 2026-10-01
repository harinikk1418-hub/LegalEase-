@echo off
start "backend" cmd /k uvicorn legalEaseAPI.main:app --reload --port 8000
streamlit run frontend/app.py
