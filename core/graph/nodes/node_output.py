import json
from core.graph.state import ReviewState


def node_output(state: ReviewState) -> dict:
    output = {
        "metrics_summary": state.get('metrics'),
        "quality_gates": state.get('quality_gates'),
        "findings": state.get("ai_report")
    }
    return {"output": output}