from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from agents.state import DueDiligenceState
from config.prompts import SUMMARY_PROMPT
from config.settings import settings


def executive_summary_node(state: DueDiligenceState) -> dict:
    llm = ChatOpenAI(model=settings.DEFAULT_LLM_MODEL, temperature=0.2, api_key=settings.OPENAI_API_KEY)
    chain = ChatPromptTemplate.from_template(SUMMARY_PROMPT) | llm

    response = chain.invoke({
        "target_company": state.get("target_company") or "Target Entity",
        "risk_matrix": state.get("risk_matrix", {}),
        "legal_findings": state.get("legal_findings", {}),
        "financial_findings": state.get("financial_findings", {}),
        "compliance_findings": state.get("compliance_findings", {})
    })

    return {"executive_summary": response.content}