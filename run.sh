#!/usr/bin/env bash
# Starts FastAPI backend (8000) and Streamlit frontend (8501)
uvicorn legalEaseAPI.main:app --reload --port 8000 &
BACK=$!
trap "kill $BACK" EXIT
streamlit run frontend/app.py
