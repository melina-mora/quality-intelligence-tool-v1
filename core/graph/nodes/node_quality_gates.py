from core.graph.state import ReviewState
from core.analyzers import quality_gates
from time import time

def node_quality_gates(state: ReviewState) -> dict:
    gates = quality_gates.QualityGates(state.get('metrics'), state.get('bugs'))
    return {"quality_gates": gates.gates}