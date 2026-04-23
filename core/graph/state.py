from typing import TypedDict

class ReviewState(TypedDict):
    #Inputs
    xml_path: str
    csv_path: str

    # Outputs
    report: dict
    bugs: list
    metrics: dict
    quality_gates: dict
    ai_report: dict
    output: dict