import datetime
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

TEMPLATES_DIR = Path(__file__).parent.parent / "templates"


def build_report(metrics: dict, quality_gates: list, findings: list, report_date=datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S"), suite_name="demo_suite") -> str:
    env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)), autoescape=True)
    template = env.get_template("report.html")
    return template.render(
        metrics=metrics,
        quality_gates=quality_gates,
        findings=findings,
        report_date=report_date,
        suite_name=suite_name
    )
