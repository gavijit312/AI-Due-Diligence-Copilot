from typing import List, Dict, Any, Optional
from typing_extensions import TypedDict


class AgentFinding(TypedDict):
    domain: str
    risk_level: str
    summary: str
    details: List[str]
    citations: List[Dict[str, Any]]


class DueDiligenceState(TypedDict):
    session_id: str
    uploaded_files: List[str]
    target_company: Optional[str]
    query: Optional[str]
    legal_findings: Optional[AgentFinding]
    financial_findings: Optional[AgentFinding]
    compliance_findings: Optional[AgentFinding]
    risk_matrix: Optional[Dict[str, Any]]
    executive_summary: Optional[str]
    errors: List[str]