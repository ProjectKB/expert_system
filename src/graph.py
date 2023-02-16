from dataclasses import dataclass
from src.rule import Rule
from src.interpreter import Interpreter


@dataclass
class Graph:
    query: str
    rules: list[Rule]

    def show_graph(self):
        print(self.query)
        self.__travel_graph(self.rules, 0)

    def __travel_graph(self, rules: list[Rule], depth):
        for rule in rules:
            print(f"{'-' * (depth + 1)}{rule}")
            if rule.children:
                self.__travel_graph(rule.children, depth + 1)

    def resolve_graph(self, rules: list[Rule], interpreter: Interpreter, facts: dict[str: int]):
        for rule in rules:
            if rule.children:
                self.resolve_graph(rule.children, interpreter, facts)
            if not rule.visited:
                rule.infer(interpreter, facts)
