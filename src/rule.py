from dataclasses import dataclass
from src.interpreter import Interpreter
from src.inverter import Inverter
from src.error import Error


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
        res_premised = interpreter.visit(self.premised, facts)

        if res_premised.value == 1:
            conclusion_memory = {fact: facts[fact] for fact in self.conclusion_facts}
            for fact in self.conclusion_facts:
                if facts.get(f'{fact}_inverted'):
                    Error.throw(Error.FAIL, Error.LOGIC_ERROR, f"There is something wrong in the logic for this rule: {self.__repr__()}")
                facts[fact] = 1
            res_conclusion = interpreter.visit(self.conclusion, facts)
            premised_memory = {fact: facts[fact] for fact in self.premised_facts}

            # handle conclusion neg case
            if res_conclusion.value == 0:
                inverter = Inverter()
                inverter.invert(self.conclusion)
                for fact in inverter.to_invert:
                    if conclusion_memory[fact] == 1:
                        Error.throw(Error.FAIL, Error.LOGIC_ERROR, f"There is something wrong in the logic for this rule: {self.__repr__()}")
                    facts[fact] = 0
                    facts[f'{fact}_inverted'] = True

            intersections = list(set(self.premised_facts).intersection(set(self.conclusion_facts)))
            for intersection in intersections:
                if premised_memory[intersection] != facts[intersection]:
                    Error.throw(Error.FAIL, Error.LOGIC_ERROR, f"There is something wrong in the logic for this rule: {self.__repr__()}")
