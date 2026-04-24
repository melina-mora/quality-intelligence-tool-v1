from time import time
from core.graph.state import ReviewState
from core.analyzers import test_run_analyzer


def node_ai_analyzer(state: ReviewState) -> dict:
    t1 = time()
    print("DEBUG: node_ai_analyzer started")
    ai_report = test_run_analyzer.analyze(state.get('report').get('test_cases'))
    t2 = time()
    print(f"DEBUG: node_ai_analyzer took: {t2-t1} seconds ")
    return {"ai_report": ai_report}