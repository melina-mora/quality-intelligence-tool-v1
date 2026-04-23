from graph.state import ReviewState
from analyzers import test_run_analyzer

def node_ai_analyzer(state: ReviewState) -> dict:
    ai_report = test_run_analyzer.analyze(state.get('report').get('test_cases'))
    return {"ai_report": ai_report}