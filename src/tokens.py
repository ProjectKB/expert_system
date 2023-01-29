from enum import Enum, auto
from dataclasses import dataclass


class TokenType(Enum):
    LETTER = auto()
    AND = auto()
    OR = auto()
    XOR = auto()
    NOT = auto()
    IMPLIES = auto()
    EQUIV = auto()
    LPAREN = auto()
    RPAREN = auto()


TOKEN_HASH = {
    '+': TokenType.AND,
    '|': TokenType.OR,
    '^': TokenType.XOR,
    '!': TokenType.NOT,
    '(': TokenType.LPAREN,
    ')': TokenType.RPAREN,
}


@dataclass
class Token:
    type: TokenType
    value: any = None

    def __repr__(self):
        return self.type.name + (f":{self.value}" if self.value is not None else "")
