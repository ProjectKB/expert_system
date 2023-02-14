from dataclasses import dataclass
from src.rule import Rule


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
