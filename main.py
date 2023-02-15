import argparse as a

from src.parser import parse
from src.interpreter import Interpreter


if __name__ == '__main__':
    argparse = a.ArgumentParser()
    argparse.add_argument("file", help="file containing the system")

    args = argparse.parse_args()

    system = parse(args.file)
    # print(system)
    # system.show_graph()
    rule = system.ruleset[0].premised
    interpreter = Interpreter()

    res = interpreter.visit(rule, system.facts)

    print(res)

