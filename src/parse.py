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


def parse(args) -> System:
    data = {
        'ruleset': [],
        'facts': {'known': {}, 'unknown': {}},
        'queries': "",
    }

    if not Path(args.file).is_file():
        Error.throw(Error.FAIL, Error.FILE_NOT_FOUND_ERROR, f"file not found: {args.file}")
    try:
        with open(args.file, 'r') as f:
            rules = []
            facts_checker = {'defined': False}

            for line in f.readlines():
                line = line.removesuffix("\n")
                line = __remove_comment(line)
                if line != "":
                    __split_patterns(line, data, rules, facts_checker)

        __check_repetition(rules, 'rules')
        __check_repetition(data['queries'], 'queries')

        if not data['queries'] or not data['ruleset'] or not facts_checker['defined']:
            Error.throw(Error.FAIL, Error.FILE_FORMAT_ERROR, "you must define a ruleset, facts and at least one query")
    except UnicodeDecodeError:
        Error.throw(Error.FAIL, Error.UNICODE_DECODE_ERROR, f"'utf-8' codec can't decode byte")
    except PermissionError:
        Error.throw(Error.FAIL, Error.PERMISSION_ERROR, f"permission denied: {args.file}")

    __prepare_ruleset(data)

    return System(data['ruleset'], data['facts']['known'] | data['facts']['unknown'], data['queries'], args)


def __split_patterns(line: str, data: dict, rules: list[str], facts_checker: set) -> None:
    if f := re.match(FACTS_PATTERN, line):
        if data['queries'] or not data['ruleset']:
            Error.throw(Error.FAIL, Error.FILE_FORMAT_ERROR, "format has to be ruleset, then facts, then queries")
        elif not data['facts']['known']:
            facts_checker['defined'] = True
            facts = f.group()[1:]
            __check_repetition(facts, 'facts')
            data['facts']['known'] = {letter: 1 for letter in facts}
        else:
            Error.throw(Error.FAIL, Error.FILE_FORMAT_ERROR, "initial facts cannot be set several times")
    elif q := re.match(QUERIES_PATTERN, line):
        if not facts_checker['defined'] or not data['ruleset']:
            Error.throw(Error.FAIL, Error.FILE_FORMAT_ERROR, "format has to be ruleset, then facts, then queries")
        elif not data['queries']:
            data['queries'] = q.group()[1:]
        else:
            Error.throw(Error.FAIL, Error.FILE_FORMAT_ERROR, "queries cannot be set several times")
    else:
        if facts_checker['defined'] or data['queries']:
            Error.throw(Error.FAIL, Error.FILE_FORMAT_ERROR, "format has to be ruleset, then facts, then queries")
        elif EQUIV not in line and len(rule_materials := line.split(IMPLIES)) == 2:
            rules.append(line)
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
    if {"|", "^"}.intersection(set(list(conclusion))):
        Error.throw(Error.FAIL, Error.FILE_FORMAT_ERROR, f"rule syntax error: {conclusion}")
    elif not len(premised.strip()) or not len(conclusion.strip()):
        Error.throw(Error.FAIL, Error.FILE_FORMAT_ERROR, f"rule syntax error: {line}")
    return {'premised': premised, 'op': op, 'conclusion': conclusion}


def __parse_rule(text: str, data: dict, rule_facts: list) -> any:
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


def __check_repetition(data: any, case: str) -> None:
    if len(data) != len(set(data)):
        Error.throw(Error.FAIL, Error.FILE_FORMAT_ERROR, f"syntax error: repetition are not allowed for {case}")
