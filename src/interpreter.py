from nodes import *
from values import Bit


class Interpreter:
    def visit(self, node: any) -> any:
        method_name = f'__visit_{type(node).__name__}'
        method = getattr(self, method_name)
        return method(node)

    def __visit_LetterNode(self, node: LetterNode) -> Bit:
        return Bit(node.value)

    def __visit_NotNode(self, node: NotNode) -> Bit:
        return Bit(~node.value)

    def __visit_AndNode(self, node: AndNode) -> Bit:
        return Bit(node.node_a & node.node_b)

    def __visit_OrNode(self, node: OrNode) -> Bit:
        return Bit(node.node_a | node.node_b)

    def __visit_XorNode(self, node: XorNode) -> Bit:
        return Bit(node.node_a ^ node.node_b)
