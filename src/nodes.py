from dataclasses import dataclass


@dataclass
class LetterNode:
    value: str

    def __repr__(self):
        return f"{self.value}"


@dataclass
class AndNode:
    node_a: any
    node_b: any

    def __repr__(self):
        return f"({self.node_a} & {self.node_b})"


@dataclass
class OrNode:
    node_a: any
    node_b: any

    def __repr__(self):
        return f"({self.node_a} | {self.node_b})"


@dataclass
class XorNode:
    node_a: any
    node_b: any

    def __repr__(self):
        return f"({self.node_a} ^ {self.node_b})"


@dataclass
class NotNode:
    node: any

    def __repr__(self):
        return f"!{self.node}"


@dataclass
class ImpliesNode:
    node_a: any
    node_b: any

    def __repr__(self) -> str:
        return f"({self.node_a} => {self.node_b})"
