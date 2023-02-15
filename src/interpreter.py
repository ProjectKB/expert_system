from src.nodes import *
from src.values import Bit


class Interpreter:
    def visit(self, node: any, facts: dict[str: int]) -> any:
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name)
        return method(node, facts)

    @staticmethod
    def visit_LetterNode(node: LetterNode, facts: dict[str: int]) -> Bit:
        return Bit(facts[node.value])

    def visit_NotNode(self, node: NotNode, facts: dict[str: int]) -> Bit:
        return Bit(int(not bool(self.visit(node.node, facts).value)))

    def visit_AndNode(self, node: AndNode, facts: dict[str: int]) -> Bit:
        return Bit(self.visit(node.node_a, facts).value & self.visit(node.node_b, facts).value)

    def visit_OrNode(self, node: OrNode, facts: dict[str: int]) -> Bit:
        return Bit(self.visit(node.node_a, facts).value | self.visit(node.node_b, facts).value)

    def visit_XorNode(self, node: XorNode, facts: dict[str: int]) -> Bit:
        return Bit(self.visit(node.node_a, facts).value ^ self.visit(node.node_b, facts).value)
