from src.tokens import TokenType
from src.nodes import *


class RuleParser:
    tokens: any
    current_token: any

    def __init__(self, tokens: any):
        self.tokens = iter(tokens)
        self.__advance()

    def __advance(self) -> None:
        try:
            self.current_token = next(self.tokens)
        except StopIteration:
            self.current_token = None

    def parse(self) -> any:
        if self.current_token is None:
            return None

        result = self.__expr()

        if self.current_token is not None:
            raise Exception("Invalid Syntax Global")

        return result

    def __expr(self) -> any:
        result = self.__expr2()

        while self.current_token is not None and self.current_token.type == TokenType.XOR:
            if self.current_token.type == TokenType.XOR:
                self.__advance()
                result = XorNode(result, self.__expr2())

        return result

    def __expr2(self) -> any:
        result = self.__term()

        while self.current_token is not None and self.current_token.type == TokenType.OR:
            if self.current_token.type == TokenType.OR:
                self.__advance()
                result = OrNode(result, self.__term())

        return result

    def __term(self) -> any:
        result = self.__factor()

        while self.current_token is not None and self.current_token.type == TokenType.AND:
            if self.current_token.type == TokenType.AND:
                self.__advance()
                result = AndNode(result, self.__factor())

        return result

    def __factor(self) -> any:
        token = self.current_token

        if token.type == TokenType.LPAREN:
            self.__advance()
            result = self.__expr()
            if self.current_token is None or self.current_token.type != TokenType.RPAREN:
                raise Exception("RPARENT ERROR OR NULL ERROR")
            self.__advance()
            return result
        elif token.type == TokenType.LETTER:
            self.__advance()
            return LetterNode(token.value)
        elif token.type == TokenType.NOT:
            self.__advance()
            return NotNode(self.__factor())
        raise Exception("Invalid Syntax Factor")
