from graph.state import ReviewState
import json

def node_output(state: ReviewState) -> dict:
    output = {
        "metrics_summary": state.get('metrics'),
        "quality_gates": state.get('quality_gates'),
        "ai_analysis": state.get("ai_report")
    }
    return {"output": json.dumps(output)}