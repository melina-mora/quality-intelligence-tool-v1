import argparse
from datetime import datetime
from core.graph.graph import build_graph
from core import report_builder
from core.graph.state import ReviewState


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-xml", type=str, help="Path to XML file", required=True)
    parser.add_argument("--input-bug-list", type=str, help="Path to bugs CSV file", required=True)
    parser.add_argument("--output", type=str, help="Where to store the output report", default="reports")
    parser.add_argument("--format", type=str, choices=['html', 'markdown'], default='html', help="Output format type")

    args = parser.parse_args()

    input_state: ReviewState = {
        "xml_path": args.input_xml,
        "csv_path": args.input_bug_list
    } #type: ignore

    compiled_graph = build_graph()
    result = compiled_graph.invoke(input_state)
    output = result.get("output")

    metrics = output.get("metrics_summary")
    quality_gates = output.get("quality_gates")
    ai_analysis = output.get("findings")

    report_date = datetime.now().strftime("%Y-%m-%d_%H%M%S")

    with open(f'reports/test_analysis_{report_date}.md', mode="w", encoding='utf-8') as f:
        content = report_builder.build_report(metrics, quality_gates, ai_analysis, report_date=report_date)
        f.write(content)

if __name__ == "__main__":
    main()
