from core.graph.state import ReviewState
from core.analyzers import metrics

def node_metrics(state: ReviewState) -> dict:
    summary = metrics.Metrics(state.get('report')).get_summary()
    return {"metrics": summary}