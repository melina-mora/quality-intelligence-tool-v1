from core.graph.state import ReviewState
from core.analyzers import test_run_analyzer
from time import time

def node_ai_analyzer(state: ReviewState) -> dict:
    print(f"DEBUG: node_ai_analyzer start: {round(time(),2)} seconds ")
    ai_report = test_run_analyzer.analyze(state.get('report').get('test_cases'))
    print(f"DEBUG: node_ai_analyzer end: {round(time(),2)} seconds")
    return {"ai_report": ai_report}