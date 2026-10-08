#!/bin/bash
# Mac/Linux: starts backend + frontend together
uvicorn legalEaseAPI.main:app --reload --port 8000 &
streamlit run frontend/app.py
