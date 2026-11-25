import json
from dataclasses import dataclass, asdict


@dataclass
class Message:
    sender: int
    round_number: int
    values: list
    event_type: str = "CONSENSUS_UPDATE"

    def serialize(self):
        return json.dumps(asdict(self)).encode("utf-8")

    @staticmethod
    def deserialize(data):
        obj = json.loads(data.decode("utf-8"))
        return Message(**obj)