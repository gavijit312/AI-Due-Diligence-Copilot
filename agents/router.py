from agents.state import DueDiligenceState


def route_supervisor_node(state: DueDiligenceState) -> dict:
    """Supervisory node initializing default state arrays if missing."""
    return {
        "errors": state.get("errors") or []
    }