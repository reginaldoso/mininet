import random
import time


class FailureInjector:

    def __init__(
        self,
        mode="none",
        fail_nodes=None,
        fail_count=0,
        fail_round=1
    ):

        self.mode = mode
        self.fail_nodes = fail_nodes or []
        self.fail_count = fail_count
        self.fail_round = fail_round

        self.injected = False

    def select_nodes(self, total_nodes):

        if self.mode == "none":
            return []

        if self.mode == "manual":
            return self.fail_nodes

        if self.mode == "random":

            if self.fail_count > total_nodes:
                raise ValueError("Quantidade de falhas inválida")

            return random.sample(
                range(1, total_nodes + 1),
                self.fail_count
            )

        raise ValueError("Modo de falha desconhecido")

    def should_inject(self, current_round):

        return (
            not self.injected
            and current_round == self.fail_round
            and self.mode != "none"
        )

    def mark_injected(self):
        self.injected = True
