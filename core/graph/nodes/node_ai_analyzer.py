from core.graph.state import ReviewState
from core.analyzers import ai_analyzer


def node_ai_analyzer(state: ReviewState) -> dict:
    ai_report = ai_analyzer.analyze(state.get('report').get('test_cases'))
    return {"ai_report": ai_report}