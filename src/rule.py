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
    children: list | None = None

    def __repr__(self) -> str:
        return f"{self.premised} {self.op} {self.conclusion}"

    def infer(self, interpreter: Interpreter, facts: dict[str: int]):
        res_premised = interpreter.visit(self.premised, facts)

        if res_premised.value == 1:
            conclusion_memory = {fact: facts[fact] for fact in self.conclusion_facts}
            for fact in self.conclusion_facts:
                # handle when facts have already been inverted (cf multi_conclusions_negation)
                if not facts.get(f'{fact}_inverted'):
                    facts[fact] = 1

            res_conclusion = interpreter.visit(self.conclusion, facts)

            # handle conclusion inverted facts
            if res_conclusion.value == 0:
                for fact in self.conclusion_facts:
                    # fact has already been inverted in anterior rule (cf negation3.1)
                    if facts.get(f'{fact}_inverted'):
                        Error.throw(Error.FAIL, Error.LOGIC_ERROR, f"In rule \"{self.__repr__()}\" fact \"{fact}\" has already been inverted in anterior rule")

                inverter = Inverter()
                inverter.invert(self.conclusion)
                for fact in inverter.to_invert:
                    # fact has to be true because of anterior rule/fact (cf negation3.2/negation4/negation5)
                    if conclusion_memory[fact] == 1:
                        Error.throw(Error.FAIL, Error.LOGIC_ERROR, f"In rule \"{self.__repr__()}\" fact \"{fact}\" can't be inverted because it has been defined as true in anterior rule or initial/premised facts")
                    facts[fact] = 0
                    facts[f'{fact}_inverted'] = True
