class RoundManager:

    def __init__(self, fault_limit):
        self.fault_limit = fault_limit
        self.current_round = 1
        self.total_rounds = fault_limit + 1

    def has_next_round(self):
        return self.current_round <= self.total_rounds

    def advance(self):
        self.current_round += 1

    def get_current_round(self):
        return self.current_round
