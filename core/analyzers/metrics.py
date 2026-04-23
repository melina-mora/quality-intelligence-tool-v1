
class Metrics():
    def __init__(self, report):
        self.report = report
        self.summary = self.get_summary()

    def calc_pass_rate(self):
        return round((self.report['passed'] / self.report['total_tests']) * 100,2)

    def calc_avg_time_testcases(self):
        return round(self.report['total_duration'] / self.report['total_tests'],3)
    
    def calc_slowest_testcase(self):
        test_cases = self.report['test_cases']
        slowest_testcase = test_cases[0]
        duration = float(test_cases[0]['duration'])

        for tc in test_cases[1:]:
            test_time = float(tc['duration'])
            if test_time > duration:
                slowest_testcase = tc
                duration = test_time

        return {"name": slowest_testcase['name'], "duration": duration}

    def calc_most_problematic_testsuite(self):
        failures_by_suite = {}
        for tc in self.report['test_cases']:
            if tc['status'] == 'Failed':
                classname = tc['classname']
                failures_by_suite[classname] = failures_by_suite.get(classname, 0) + 1

        if not failures_by_suite:
            return None

        return max(failures_by_suite, key=lambda k: failures_by_suite[k])

    def get_summary(self):
        return {
                "avg_total_duration": self.calc_avg_time_testcases(),
                "test_run_pass_rate": self.calc_pass_rate(),
                "slowest_testcase": self.calc_slowest_testcase(),
                "most_problematic_testsuite": self.calc_most_problematic_testsuite()
        }