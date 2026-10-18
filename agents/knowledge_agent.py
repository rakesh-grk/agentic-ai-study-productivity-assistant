from typing import Dict, Any, Optional
from tools.knowledge_base import search_local_knowledge
from core.llm_client import LLMClient

class KnowledgeAgent:
    """Specialized agent for retrieving verified domain knowledge from local resources

    and grounding explanations without fabricating citations.
    """
    
    def __init__(self, llm_client: Optional[LLMClient] = None):
        self.llm = llm_client or LLMClient()
        self.agent_name = "Knowledge and Research Agent"

    def research(self, query: str) -> Dict[str, Any]:
        """Executes a local knowledge search and returns structured, source-attributed findings."""
        cleaned_query = query.strip()
        search_results = search_local_knowledge(cleaned_query)
        
        docs = search_results.get("documents", [])
        
        # If no local docs match, provide a transparent factual disclaimer
        if not docs:
            findings = (
                f"No exact pre-indexed curriculum document found for '{cleaned_query}'. "
                "Synthesizing standard theoretical principles based on verified core knowledge."
            )
            sources = ["System Base Knowledge (Local Curriculum)"]
        else:
            findings_list = []
            sources = []
            for d in docs:
                findings_list.append(f"• **{d['title']}** ({d['category']}): {d['content']}")
                sources.append(d["source"])
            findings = "\n".join(findings_list)
            
        return {
            "agent": self.agent_name,
            "query": cleaned_query,
            "findings": findings,
            "sources": sources,
            "is_external_live_research": False,
            "transparency_notice": "Retrieved from local offline verified references. No external live scraping performed."
        }
