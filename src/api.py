import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from fastapi import FastAPI
from query import ask_question

app = FastAPI()

@app.get("/")
def root():
    return {"message": "RAG SOP Assistant API is running"}

@app.get("/ask")
def ask(q: str):
    return ask_question(q)