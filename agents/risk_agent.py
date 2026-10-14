import json
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from agents.state import DueDiligenceState
from config.prompts import RISK_SYNTHESIS_PROMPT
from config.settings import settings


def risk_assessment_node(state: DueDiligenceState) -> dict:
    llm = ChatOpenAI(model=settings.DEFAULT_LLM_MODEL, temperature=0.0, api_key=settings.OPENAI_API_KEY)
    chain = ChatPromptTemplate.from_template(RISK_SYNTHESIS_PROMPT) | llm

    response = chain.invoke({
        "legal_findings": json.dumps(state.get("legal_findings", {})),
        "financial_findings": json.dumps(state.get("financial_findings", {})),
        "compliance_findings": json.dumps(state.get("compliance_findings", {}))
    })

    try:
        matrix = json.loads(response.content)
    except Exception:
        matrix = {"overall_risk_score": "HIGH", "raw_output": response.content}

    return {"risk_matrix": matrix}