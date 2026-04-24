import json
import argparse
import webbrowser
from pathlib import Path
from datetime import datetime
from core.graph.graph import build_graph
from core import report_builder
from core.graph.state import ReviewState

CACHE_PATH = "reports/last_run.json"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-xml", type=str, help="Path to XML file")
    parser.add_argument("--input-bug-list", type=str, help="Path to bugs CSV file")
    parser.add_argument("--output", type=str, help="Where to store the output report", default="reports")
    parser.add_argument("--rebuild", action="store_true", help="Re-render the last run without calling the model")

    args = parser.parse_args()

    if args.rebuild:
        with open(CACHE_PATH, encoding="utf-8") as f:
            output = json.load(f)
    else:
        if not args.input_xml or not args.input_bug_list:
            parser.error("--input-xml and --input-bug-list are required unless using --rebuild")

        input_state: ReviewState = {
            "xml_path": args.input_xml,
            "csv_path": args.input_bug_list
        } #type: ignore

        compiled_graph = build_graph()
        result = compiled_graph.invoke(input_state)
        output = result["output"]

        with open(CACHE_PATH, mode="w", encoding="utf-8") as f:
            json.dump(output, f, indent=2)

    metrics = output.get("metrics_summary")
    quality_gates = output.get("quality_gates")
    findings = output.get("findings")

    report_date = datetime.now().strftime("%Y-%m-%d_%H%M%S")

    with open(f'{args.output}/test_analysis_{report_date}.html', mode="w", encoding='utf-8') as f:
        content = report_builder.build_report(metrics, quality_gates, findings, report_date=report_date)
        f.write(content)

    report_path = Path(f'{args.output}/test_analysis_{report_date}.html').resolve()
    print(f"Report saved: {report_path}")
    webbrowser.open(report_path.as_uri())

if __name__ == "__main__":
    main()
