from langgraph.graph import StateGraph, START, END
from agents.state import DueDiligenceState
from agents.legal_agent import legal_analysis_node
from agents.financial_agent import financial_analysis_node
from agents.compliance_agent import compliance_analysis_node
from agents.risk_agent import risk_assessment_node
from agents.summary_agent import executive_summary_node


def build_due_diligence_graph():
    workflow = StateGraph(DueDiligenceState)

    workflow.add_node("legal_agent", legal_analysis_node)
    workflow.add_node("financial_agent", financial_analysis_node)
    workflow.add_node("compliance_agent", compliance_analysis_node)
    workflow.add_node("risk_agent", risk_assessment_node)
    workflow.add_node("summary_agent", executive_summary_node)

    # Fan out in parallel
    workflow.add_edge(START, "legal_agent")
    workflow.add_edge(START, "financial_agent")
    workflow.add_edge(START, "compliance_agent")

    # Fan into Risk Engine
    workflow.add_edge("legal_agent", "risk_agent")
    workflow.add_edge("financial_agent", "risk_agent")
    workflow.add_edge("compliance_agent", "risk_agent")

    # Conclude with Executive Summary
    workflow.add_edge("risk_agent", "summary_agent")
    workflow.add_edge("summary_agent", END)

    return workflow.compile()