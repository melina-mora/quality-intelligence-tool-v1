import datetime

def build_report(metrics: dict, quality_gates: list, findings: list, report_date=datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S"), suite_name="demo_suite") -> str:
    lines = []

    # Header
    lines.append("# Quality Intelligence Report")
    lines.append(f"**Run date:** {report_date}")
    lines.append(f"**Suite:** {suite_name}/tests/")
    lines.append("")

    # Section 1: Metrics
    lines.append("## Metrics Summary")
    lines.append(f"- Average runtime per test: {metrics['avg_total_duration']}s")
    lines.append(f"- Test run pass rate: {metrics['test_run_pass_rate']}%")
    lines.append(f"- Most problematic test suite: {metrics['most_problematic_testsuite']}")
    lines.append(f"- Slowest test case: {metrics['slowest_testcase']['name']} ({metrics['slowest_testcase']['duration']}s)")
    lines.append("")

    # Section 2: Quality Gates
    lines.append("## Quality Gates")
    lines.append("| Evaluation | Expected | Actual | Result |")
    lines.append("|---|---|---|---|")
    for gate in quality_gates:
        lines.append(f"| {gate['name']} | {gate['threshold']} | {gate['actual']} | {gate['result']} |")
    lines.append("")

    # Section 3: AI Analysis
    lines.append("## AI Analysis")
    lines.append(str(findings))

    return "\n".join(lines)