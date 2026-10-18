import re
from typing import List, Dict, Any, Optional

# Verified local knowledge repository (Offline verifiable documents)
_LOCAL_KNOWLEDGE_DOCS = [
    {
        "id": "agentic-ai-foundations",
        "title": "Agentic AI Architecture and Autonomous Workflows",
        "category": "Artificial Intelligence",
        "source": "Local Reference: Agentic AI Systems Architecture Guide (Course Core)",
        "content": (
            "Agentic AI systems move beyond passive conversational models by incorporating goal formulation, "
            "multi-step planning, tool invocation, persistent memory, and iterative critique loops. "
            "Key patterns include ReAct (Reasoning + Acting), Plan-and-Solve (generating an explicit plan before "
            "subtask execution), and Multi-Agent Orchestration where specialized agents (Planner, Researcher, Executor, Critic) "
            "collaborate under an Orchestrator."
        ),
        "keywords": ["agent", "agentic", "react", "planner", "critic", "orchestrator", "tool calling", "autonomous"]
    },
    {
        "id": "study-methodologies",
        "title": "Evidence-Based Learning Strategies: Active Recall & Spaced Repetition",
        "category": "Productivity Science",
        "source": "Local Reference: Cognitive Science & Evidence-Based Study Techniques",
        "content": (
            "Decades of cognitive psychology indicate that Active Recall (testing retrieval rather than re-reading) "
            "and Spaced Repetition (expanding review intervals following the Ebbinghaus forgetting curve) yield "
            "the highest long-term retention. Complementary techniques include the Feynman Technique (simplifying "
            "concepts to teach novices) and the Pomodoro Technique (25-minute focused bursts with 5-minute restorative breaks)."
        ),
        "keywords": ["study", "active recall", "spaced repetition", "pomodoro", "feynman", "memory", "retention", "exam"]
    },
    {
        "id": "python-performance",
        "title": "Python Data Structures and Algorithmic Time Complexity",
        "category": "Computer Science",
        "source": "Local Reference: Algorithms and Python Data Structures Handbook",
        "content": (
            "In Python, standard list lookups take O(n) average time, while dict and set lookups achieve O(1) "
            "average time via hash tables. When handling FIFO queues, collections.deque provides O(1) appends and pops, "
            "avoiding the O(n) overhead of list.pop(0). Sorting in Python uses Timsort with O(n log n) worst-case time."
        ),
        "keywords": ["python", "complexity", "time complexity", "big o", "data structures", "list", "dict", "deque"]
    },
    {
        "id": "ai-verification-safety",
        "title": "Verification, Guardrails, and Hallucination Mitigation in LLMs",
        "category": "AI Safety",
        "source": "Local Reference: LLM Verification and Secure Tool Use Standards",
        "content": (
            "To safeguard autonomous systems against hallucinations and prompt injection: "
            "1. Enforce strict tool allowlists with AST or schema validation rather than eval(). "
            "2. Implement independent Critic agents to verify factual grounding against retrieved sources. "
            "3. Enforce deterministic bounded retry limits to prevent infinite recursion or agent deadlock."
        ),
        "keywords": ["verification", "critic", "hallucination", "guardrails", "security", "safety", "ast"]
    }
]

def search_local_knowledge(query: str, max_results: int = 3) -> Dict[str, Any]:
    """Retrieves relevant local knowledge snippets based on keyword and semantic match.
    
    Clearly labels results as local offline reference material.
    """
    cleaned = query.lower()
    tokens = re.findall(r"\w+", cleaned)
    
    scored_docs: List[tuple] = []
    for doc in _LOCAL_KNOWLEDGE_DOCS:
        score = 0
        # Title match
        if any(tok in doc["title"].lower() for tok in tokens):
            score += 3
        # Keywords match
        for kw in doc["keywords"]:
            if any(tok in kw.lower() or kw.lower() in cleaned for tok in tokens):
                score += 2
        # Content match
        for tok in tokens:
            if len(tok) > 3 and tok in doc["content"].lower():
                score += 1
                
        if score > 0:
            scored_docs.append((score, doc))
            
    scored_docs.sort(key=lambda x: x[0], reverse=True)
    results = [doc for _, doc in scored_docs[:max_results]]
    
    return {
        "success": True,
        "query": query,
        "results_count": len(results),
        "documents": results,
        "source_type": "Verified Local Knowledge Base (No live external scraping)",
        "disclaimer": "All retrieved information originates from verified local curriculum documentation."
    }
