import json
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from agents.state import DueDiligenceState
from config.prompts import COMPLIANCE_PROMPT
from config.settings import settings
from core.vector_store import vector_service


def compliance_analysis_node(state: DueDiligenceState) -> dict:
    docs = vector_service.similarity_search_by_category(
        query="regulatory licenses, data privacy violations, sanctions, active litigation, environmental compliance",
        category="compliance",
        k=6
    )
    context = "\n---\n".join([f"Source: {d.metadata.get('source')} (Page {d.metadata.get('page')})\n{d.page_content}" for d in docs])

    llm = ChatOpenAI(model=settings.DEFAULT_LLM_MODEL, temperature=0.1, api_key=settings.OPENAI_API_KEY)
    chain = ChatPromptTemplate.from_template(COMPLIANCE_PROMPT) | llm
    response = chain.invoke({"context": context})

    try:
        findings = json.loads(response.content)
    except Exception:
        findings = {"domain": "Compliance", "risk_level": "UNKNOWN", "summary": response.content, "details": [], "citations": []}

    return {"compliance_findings": findings}