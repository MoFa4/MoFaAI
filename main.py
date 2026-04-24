# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from intent_classifier import detect_intent
from prompt_templates import PROMPTS
from memory import get_session, save_message
import requests, re

app = FastAPI(title="MofaAI v0.2.0")
OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "qwen2.5:1.5b"

class QueryRequest(BaseModel):
    query: str
    session_id: str = "default"

class QueryResponse(BaseModel):
    intent: str
    response: str
    reasoning_trace: str | None = None
    confidence_note: str | None = None
    session_id: str

def call_ollama(messages: list) -> str:
    res = requests.post(OLLAMA_URL, json={"model": MODEL_NAME, "messages": messages, "stream": False}, timeout=90)
    res.raise_for_status()
    return res.json()["message"]["content"].strip()

@app.post("/ask", response_model=QueryResponse)
async def ask(req: QueryRequest):
    try:
        intent = detect_intent(req.query)
        history = get_session(req.session_id)
        context = "\n".join(history) if history else "No prior context."
        
        sys_prompt = f"You are MofaAI. Intent: {intent.upper()}. Context: {context}. Be concise. Flag uncertainty clearly."
        messages = [{"role": "system", "content": sys_prompt}, {"role": "user", "content": req.query}]
        
        raw = call_ollama(messages)
        sentences = re.split(r'(?<=[.!?]) +', raw)
        reasoning_trace = sentences[0] if len(sentences) > 1 else None
        response = " ".join(sentences[1:]) if len(sentences) > 1 else raw
        
        uncertain_kw = ["not sure", "uncertain", "might be", "could be", "i don't know", "lack data"]
        confidence_note = "️ Low confidence - verify critical info" if any(k in raw.lower() for k in uncertain_kw) else None
        
        save_message(req.session_id, "user", req.query)
        save_message(req.session_id, "assistant", response)
        
        return QueryResponse(intent=intent, response=response, reasoning_trace=reasoning_trace, confidence_note=confidence_note, session_id=req.session_id)
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))
