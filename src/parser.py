from pathlib import Path
import re

from src.rule import Rule
from src.error import Error
from src.lexer import Lexer
from src.rule_parser import RuleParser
from src.system import System

FACTS_PATTERN = r"^=[A-Z]*$"
QUERIES_PATTERN = r"^\?[A-Z]+$"
IMPLIES = "=>"
EQUIV = "<=>"


def parse(file_name: str) -> System:
    data = {
        'ruleset': [],
        'facts': {'known': {}, 'unknown': {}},
        'queries': "",
    }

    if not Path(file_name).is_file():
        Error.throw(Error.FAIL, Error.FILE_NOT_FOUND_ERROR, f"file not found: {file_name}")
    try:
        with open(file_name, 'r') as f:
            for line in f.readlines():
                line = line.removesuffix("\n")
                line = __remove_comment(line)
                if line != "":
                    __split_patterns(line, data)
        if not data['facts'] or not data['ruleset'] or not data['queries']:
            Error.throw(Error.FAIL, Error.FILE_FORMAT_ERROR, "you must define a ruleset, facts and at least one query")
    except UnicodeDecodeError:
        Error.throw(Error.FAIL, Error.UNICODE_DECODE_ERROR, f"'utf-8' codec can't decode byte")
    except PermissionError:
        Error.throw(Error.FAIL, Error.PERMISSION_ERROR, f"permission denied: {file_name}")

    __prepare_ruleset(data)

    return System(data['ruleset'], data['facts']['known'] | data['facts']['unknown'], data['queries'])


def __split_patterns(line: str, data: dict) -> None:
    if f := re.match(FACTS_PATTERN, line):
        if not data['facts']['known']:
            data['facts']['known'] = {letter: 1 for letter in f.group()[1:]}
        else:
            Error.throw(Error.FAIL, Error.FILE_FORMAT_ERROR, "initial facts cannot be set several times")
    elif q := re.match(QUERIES_PATTERN, line):
        if not data['queries']:
            data['queries'] = q.group()[1:]
        else:
            Error.throw(Error.FAIL, Error.FILE_FORMAT_ERROR, "queries cannot be set several times")
    else:
        if EQUIV not in line and len(rule_materials := line.split(IMPLIES)) == 2:
            data['ruleset'].append(__create_rule_or_die(rule_materials, line, IMPLIES))
        else:
            Error.throw(Error.FAIL, Error.FILE_FORMAT_ERROR, f"syntax error: {line}")


def __remove_comment(line: str) -> str:
    comment_index = line.find('#')
    if comment_index != -1:
        return line[:comment_index].strip()
    return line


def __create_rule_or_die(rule_materials: list[str], line: str, op: str) -> dict:
    premised, conclusion = rule_materials
    if not len(premised.strip()) or not len(conclusion.strip()):
        Error.throw(Error.FAIL, Error.FILE_FORMAT_ERROR, f"rule syntax error: {line}")
    return {'premised': premised, 'op': op, 'conclusion': conclusion}


def __parse_rule(text: str, data: dict, rule_facts: []) -> any:
    lexer = Lexer(text)
    tokens = lexer.generate_tokens(data, rule_facts)
    parser = RuleParser(tokens)
    return parser.parse()


def __prepare_ruleset(data: dict) -> None:
    ruleset: list[Rule] = []
    for rule in data['ruleset']:
        premised_facts = []
        conclusion_facts = []
        premised = __parse_rule(rule['premised'], data, premised_facts)
        conclusion = __parse_rule(rule['conclusion'], data, conclusion_facts)
        ruleset.append(Rule(premised, rule['op'], conclusion, premised_facts, conclusion_facts))
    data['ruleset'] = ruleset


