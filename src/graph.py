from dataclasses import dataclass
from src.rule import Rule
from src.interpreter import Interpreter


@dataclass
class Graph:
    query: str
    rules: list[Rule]

    ENDC = '\033[0m'
    WHITE = '\033[97m'
    COLORS = [
        '\033[95m',
        '\033[94m',
        '\033[96m',
        '\033[92m',
        '\033[93m',
        '\033[91m'
    ]

    def show_graph(self):
        print(f"\t{self.WHITE}[{self.query}]{self.ENDC}")
        self.__travel_graph(self.rules, 0)

    def __travel_graph(self, rules: list[Rule], depth):
        for rule in rules:
            print(f"\t{self.COLORS[depth % 6]}{'-' * (depth + 1)}{rule}{self.ENDC}")
            if rule.children:
                self.__travel_graph(rule.children, depth + 1)

    def resolve_graph(self, rules: list[Rule], interpreter: Interpreter, facts: dict[str: int]):
        for rule in rules:
            if rule.children:
                self.resolve_graph(rule.children, interpreter, facts)
            if not rule.visited:
                rule.infer(interpreter, facts)
