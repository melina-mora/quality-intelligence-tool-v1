
class QualityGates():
    def __init__(self, metrics_summary, bug_reports):
        self.metrics = metrics_summary
        self.bug_reports = bug_reports
        self.gates = self.evaluate()

    def check_pass_rate(self, treshold=80):
        actual = self.metrics['test_run_pass_rate']
        return {
            "name": "Pass rate",
            "threshold": f">={treshold}%",
            "actual": round(actual, 1),
            "result": "PASS" if actual >= treshold else "FAIL"
        }

    def check_open_critical_bugs(self, treshold=0):
        critical_open = [
            b for b in self.bug_reports
            if b['severity'].upper() == 'CRITICAL' and b['status'].upper() == 'OPEN'
        ]
        count = len(critical_open)
        return {
            "name": "Critical bugs open",
            "threshold": f"{treshold}",
            "actual": count,
            "result": "PASS" if count == treshold else "FAIL"
        }

    def check_slowest_testcase(self, treshold=5):
        slowest = self.metrics['slowest_testcase']
        duration = slowest['duration'] if slowest else 0.0
        return {
            "name": "Slowest test",
            "threshold": f"<{treshold}s",
            "actual": round(duration, 3),
            "test_id": slowest['name'] if slowest else None,
            "result": "PASS" if duration < treshold else "WARN"
        }

    def evaluate(self):
        return [
            self.check_pass_rate(),
            self.check_open_critical_bugs(),
            self.check_slowest_testcase()
        ]
