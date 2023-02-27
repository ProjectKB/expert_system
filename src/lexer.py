from collections.abc import Generator

from src.tokens import Token, TokenType, TOKEN_HASH
from src.error import Error


class Lexer:
    text: str
    current_char: str | None

    WHITESPACE = ' \n\t'
    ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    OP = "+|^()!"

    def __init__(self, text: str):
        self.text = iter(text)
        self.__advance()

    def __advance(self) -> None:
        try:
            self.current_char = next(self.text)
        except StopIteration:
            self.current_char = None

    def generate_tokens(self, data: dict, rule_facts: list[str]) -> Generator:
        while self.current_char is not None:
            if self.current_char in self.WHITESPACE:
                pass
            elif self.current_char in self.ALPHABET:
                if data['facts']['known'].get(self.current_char) is None:
                    data['facts']['unknown'][self.current_char] = 0
                rule_facts.append(self.current_char)
                yield Token(TokenType.LETTER, self.current_char)
            elif self.current_char in self.OP:
                yield Token(TOKEN_HASH[self.current_char])
            else:
                Error.throw(Error.FAIL, Error.FILE_FORMAT_ERROR, f"Illegal character '{self.current_char}'")
            self.__advance()

