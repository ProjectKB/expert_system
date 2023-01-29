from dataclasses import dataclass
from src.rule import Rule


@dataclass
class System:
    ruleset: list[Rule]
    facts_known: dict[str: int]
    facts_unknown: dict[str: int]
    queries: str

    def __repr__(self) -> str:
        repr = ""
        repr += f"facts known: {self.facts_known}\n"
        repr += f"facts unknown: {self.facts_unknown}\n"
        repr += "ruleset:\n"
        repr += ''.join([f"\t{rule}\n" for rule in self.ruleset])
        repr += f"queries: {self.queries}"
        return repr
