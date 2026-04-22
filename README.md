# 🧠 MofaAI — Intent-Aware, Absence-Aware LLM

> An experimental LLM that understands **WHY** you're asking and honestly flags **what it doesn't know**.

## ✨ Unique Features
- **Intent Detection**: Adapts reasoning style for `Learn` | `Decide` | `Create` | `Debug` queries
- **Absence Awareness**: Explicitly flags uncertainty + asks clarifying questions instead of hallucinating
- **Transparent by Design**: Built for trust, not just answers

## 🚀 Quick Start
```bash
# 1. Clone & setup
git clone https://github.com/fazil/mofaai.git
cd mofaai
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 2. Run server
uvicorn main:app --reload

# 3. Test interactively
# Visit: http://127.0.0.1:8000/docs
# Or use curl:
curl -X POST http://127.0.0.1:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"query":"Should I use Flask or FastAPI?"}'
