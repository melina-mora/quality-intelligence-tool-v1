from core.graph.state import ReviewState
from core.parsers import xml_parser

def node_xml_parser(state: ReviewState) -> dict:
    report = xml_parser.Report(state.get('xml_path')).get_final_report()
    return { "report" : report}