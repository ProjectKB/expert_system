from src.nodes import *
from src.values import Bit


class Inverter:
    to_invert: list[str] = []

    def invert(self, node: any, parent: str = 'none') -> any:
        method_name = f'invert_{type(node).__name__}'
        method = getattr(self, method_name)
        if parent == 'invert_NotNode' and method_name != 'invert_NotNode':
            self.to_invert += method(node, method_name)
        return method(node, method_name)

    @staticmethod
    def invert_LetterNode(node: LetterNode, _) -> str:
        return node.value

    def invert_NotNode(self, node: NotNode, parent) -> list[str]:
        return self.invert(node.node, parent)

    def invert_AndNode(self, node: AndNode, parent) -> list[str]:
        return [self.invert(node.node_a, parent), self.invert(node.node_b, parent)]

    def invert_OrNode(self, node: OrNode, parent) -> list[str]:
        return [self.invert(node.node_a, parent), self.invert(node.node_b, parent)]

    def invert_XorNode(self, node: XorNode, parent) -> list[str]:
        return [self.invert(node.node_a, parent), self.invert(node.node_b, parent)]
