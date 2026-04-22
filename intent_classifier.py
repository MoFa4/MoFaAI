# intent_classifier.py
def detect_intent(query: str) -> str:
    query_lower = query.lower()
    
    if any(word in query_lower for word in ["explain", "what is", "how does", "teach"]):
        return "learn"
    elif any(word in query_lower for word in ["should i", "which is better", "recommend", "choose"]):
        return "decide"
    elif any(word in query_lower for word in ["write", "create", "generate", "draft"]):
        return "create"
    elif any(word in query_lower for word in ["error", "bug", "fix", "why not working"]):
        return "debug"
    else:
        return "general"  # fallback