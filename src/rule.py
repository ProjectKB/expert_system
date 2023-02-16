from dataclasses import dataclass
from src.interpreter import Interpreter
from src.inverter import Inverter


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
        res_premised = interpreter.visit(self.premised, facts)

        if res_premised.value == 1:
            for fact in self.conclusion_facts:
                facts[fact] = 1
            res_conclusion = interpreter.visit(self.conclusion, facts)
            if res_conclusion.value == 0:
                inverter = Inverter()
                inverter.invert(self.conclusion)
                for fact in inverter.to_invert:
                    facts[fact] = 0




