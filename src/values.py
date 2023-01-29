from dataclasses import dataclass


@dataclass
class Bit:
    value: int

    def __repr__(self) -> str:
        return f"{self.value}"
