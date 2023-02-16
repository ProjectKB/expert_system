from src.rule import Rule
from src.graph import Graph
from src.interpreter import Interpreter


class System:
    ruleset: list[Rule]
    facts: dict[str: int]
    queries: str
    graph: list[Graph] = []
    interpreter: Interpreter

    def __init__(self, ruleset: list[Rule], facts: dict[str: int], queries: str):
        self.ruleset = ruleset
        self.facts = facts
        self.queries = queries
        self.interpreter = Interpreter()

        self.__connect_rules()
        self.__build_graph()

    def __repr__(self) -> str:
        repr = ""
        repr += f"facts: {self.facts}\n"
        repr += "ruleset:\n"
        repr += ''.join([f"\t{rule}\n" for rule in self.ruleset])
        repr += f"queries: {self.queries}"
        return repr

    def show_graph(self):
        print("")
        for graph in self.graph:
            graph.show_graph()
            print("")

    def __connect_rules(self):
        for rule in self.ruleset:
            for child in self.ruleset:
                if rule == child:
                    continue

                if set(rule.premised_facts).intersection(set(child.conclusion_facts)):
                    match rule.children:
                        case None:
                            rule.children = [child]
                        case _:
                            rule.children.append(child)

    def __build_graph(self):
        for query in self.queries:
            rules: list[Rule] = []

            for rule in self.ruleset:
                if query in rule.conclusion_facts:
                    rules.append(rule)
            if rules:
                self.graph.append(Graph(query, rules))

    def backward_chaining(self):
        for graph in self.graph:
            graph.resolve_graph(graph.rules, self.interpreter, self.facts)

    def get_solution(self):
        for query in list(self.queries):
            print(f"{query}:{self.facts[query]}")
