import csv
import os
import time


class MetricsCollector:

    def __init__(self, process_id, output_dir="results/metrics"):

        self.process_id = process_id
        self.output_dir = output_dir

        os.makedirs(
            output_dir,
            exist_ok=True
        )

        self.start_time = time.time()
        self.messages_sent = 0
        self.messages_received = 0

    def register_sent(self):
        self.messages_sent += 1

    def register_received(self):
        self.messages_received += 1

    def save(self, decision, rounds, success):

        elapsed = time.time() - self.start_time

        filename = os.path.join(
            self.output_dir,
            f"process_{self.process_id}.csv"
        )

        with open(
            filename,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.writer(file)

            writer.writerow([
                "process_id",
                "execution_time",
                "messages_sent",
                "messages_received",
                "rounds",
                "decision",
                "success"
            ])

            writer.writerow([
                self.process_id,
                elapsed,
                self.messages_sent,
                self.messages_received,
                rounds,
                decision,
                success
            ])
