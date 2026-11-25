import time


class FailureHandler:

    def __init__(self):
        self.failures = []

    def register_failure(self, process_id, failure_type):

        event = {
            "process_id": process_id,
            "failure_type": failure_type,
            "timestamp": time.time()
        }

        self.failures.append(event)

        print(
            f"[FAILURE] Processo {process_id}: "
            f"{failure_type}"
        )

    def get_failures(self):
        return self.failures
