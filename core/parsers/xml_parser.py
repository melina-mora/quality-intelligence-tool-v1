import xml.etree.ElementTree as ET

class Report():
    def __init__(self, xml_report_path):
        self.tree = ET.parse(xml_report_path)
        self.total_tests = 0
        self.passed = 0
        self.failures = 0
        self.total_duration = 0.0
        self.test_cases = []

    def add_test_result(self, testcase):
        is_failure = testcase.find("failure") is not None

        if is_failure:
            self.failures = self.failures + 1
        else:
            self.passed = self.passed + 1

        self.test_cases.append(
            {
                "name": testcase.attrib['name'],
                "classname": testcase.attrib['classname'],
                "duration": testcase.attrib['time'],
                "status": "Failed" if is_failure else "Pass",
                "failure_message": testcase.find("failure").attrib["message"] if is_failure else None
            }
        )
        

    def get_final_report(self):
        root = self.tree.getroot()

        for testcase in root.iter("testcase"):
            self.add_test_result(testcase)

        total_duration = 0.0
        for testsuite in root.iter("testsuite"):
            total_duration += float(testsuite.attrib["time"])

        return {
            "total_tests": len(self.test_cases),
            "passed": self.passed,
            "failures": self.failures,
            "total_duration": total_duration,
            "test_cases": self.test_cases
        }