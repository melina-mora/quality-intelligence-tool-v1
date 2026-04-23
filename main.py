import core.parsers.xml_parser as xml
import core.parsers.csv_parser as csv
import core.analyzers.metrics as metrics
import time
from core.analyzers.quality_gates import QualityGates
from core.analyzers.test_run_analyzer import analyze


def main():
    report = xml.Report('data/test_run.xml').get_final_report()
    bug_reports = csv.parse('data/bugs.csv')

    m = metrics.Metrics(report)
    gates = QualityGates(m.summary, bug_reports)

    print("=== METRICS ===")
    print(m.summary)

    print("\n=== QUALITY GATES ===")
    for gate in gates.gates:
        print(gate)

    print("\n=== AI ANALYSIS ===")
    t1 = time.time()
    print(analyze(report['test_cases']))
    t2 = time.time()
    print(f"Analysis time: {t2-t1}")

if __name__ == "__main__":
    main()
