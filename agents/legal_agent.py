import json
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from agents.state import DueDiligenceState
from config.prompts import LEGAL_PROMPT
from config.settings import settings
from core.vector_store import vector_service


def legal_analysis_node(state: DueDiligenceState) -> dict:
    docs = vector_service.similarity_search_by_category(
        query="material contracts, uncapped liability, intellectual property, termination, indemnification",
        category="legal",
        k=6
    )
    context = "\n---\n".join([f"Source: {d.metadata.get('source')} (Page {d.metadata.get('page')})\n{d.page_content}" for d in docs])

    llm = ChatOpenAI(model=settings.DEFAULT_LLM_MODEL, temperature=0.1, api_key=settings.OPENAI_API_KEY)
    chain = ChatPromptTemplate.from_template(LEGAL_PROMPT) | llm
    response = chain.invoke({"context": context})

    try:
        findings = json.loads(response.content)
    except Exception:
        findings = {"domain": "Legal", "risk_level": "UNKNOWN", "summary": response.content, "details": [], "citations": []}

    return {"legal_findings": findings}