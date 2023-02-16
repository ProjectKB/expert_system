from dataclasses import dataclass
from src.interpreter import Interpreter


@dataclass
class Rule:
    premised: any
    op: str
    conclusion: any
    premised_facts: list[str]
    conclusion_facts: list[str]
    visited: bool = False
    children: list | None = None

    def __repr__(self) -> str:
        return f"{self.premised} {self.op} {self.conclusion}"

    def infer(self, interpreter: Interpreter, facts: dict[str: int]):
        self.visited = True
        res = interpreter.visit(self.premised, facts)

        if res.value == 1:
            for fact in self.conclusion_facts:
                facts[fact] = 1

