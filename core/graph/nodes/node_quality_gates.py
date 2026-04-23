from graph.state import ReviewState
from analyzers import quality_gates

def node_quality_gates(state: ReviewState) -> dict:
    gates = quality_gates.QualityGates(state.get('metrics'), state.get('bugs'))
    return {"quality_gates": gates.gates}