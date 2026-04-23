from core.graph.state import ReviewState
from core.parsers import csv_parser

def node_csv_parser(state: ReviewState) -> dict:
    bugs = csv_parser.parse(state.get('csv_path'))
    return {"bugs": bugs}