from dataclasses import dataclass


@dataclass
class Rule:
    premised: any
    op: str
    conclusion: any
    premised_facts: list[str]
    conclusion_facts: list[str]
    visited: bool = False
    children: list | None = None

    def __repr__(self) -> str:
        return f"{self.premised} {self.op} {self.conclusion}"


