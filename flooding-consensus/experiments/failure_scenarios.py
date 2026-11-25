class FailureScenarios:

    def __init__(self, fault_limit):

        self.fault_limit = fault_limit

    def validate_failure_count(self, failures):

        if failures < 0:
            return False

        return failures <= self.fault_limit

    def classify_scenario(self, failures):

        if failures == 0:
            return "NO_FAILURE"

        if failures <= self.fault_limit:
            return "WITHIN_TOLERANCE"

        return "ABOVE_TOLERANCE"

    def describe(self, failures):

        return {
            "failures": failures,
            "fault_limit": self.fault_limit,
            "scenario": self.classify_scenario(failures),
            "within_tolerance": self.validate_failure_count(
                failures
            )
        }

"""
Esse módulo não provoca falhas automaticamente. Ele classifica os cenários. A injeção efetiva de falhas será realizada posteriormente pelo controlador dos experimentos.
"""