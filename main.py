# main.py
from fastapi import FastAPI
from pydantic import BaseModel
from intent_classifier import detect_intent
from prompt_templates import PROMPTS
from transformers import pipeline

app = FastAPI(title="MofaAI v0.0.1")

# Load lightweight local LLM (replace with Ollama/API later)
llm = pipeline("text-generation", model="Qwen/Qwen2.5-0.5B-Instruct")

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    intent: str
    response: str
    confidence_note: str | None = None
    reasoning_trace: str | None = None  # ← Add this

@app.post("/ask", response_model=QueryResponse)
async def ask(request: QueryRequest):
    # 1. Detect intent
    intent = detect_intent(request.query)
    
    # 2. Build adaptive prompt WITH reasoning instruction
    prompt_template = PROMPTS.get(intent, PROMPTS["general"])
    full_prompt = f"""Think step-by-step. Then answer.
If uncertain, explicitly say what's missing and ask a clarifying question.

{prompt_template.format(query=request.query)}"""
    
    # 3. Generate response
    result = llm(full_prompt, max_new_tokens=300, do_sample=True, temperature=0.3)[0]['generated_text']
    answer = result.replace(full_prompt, "").strip()
    
    # 4. Enhanced absence-aware flagging
    uncertainty_keywords = ["not sure", "uncertain", "might be", "could be", "i don't know", "lack information", "need more context", "unable to determine"]
    confidence_note = None
    if any(kw in answer.lower() for kw in uncertainty_keywords):
        confidence_note = "⚠️ MofaAI flagged uncertainty — verify critical info"
    
    # 5. Extract simple reasoning trace (first 2 sentences)
    sentences = answer.split('. ')
    reasoning_trace = '. '.join(sentences[:2]) + '.' if len(sentences) > 2 else None
    
    return QueryResponse(
        intent=intent,
        response=answer,
        confidence_note=confidence_note
        # We'll add reasoning_trace to the model next
    )