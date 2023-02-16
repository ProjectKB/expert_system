import argparse as a

from src.parser import parse


if __name__ == '__main__':
    argparse = a.ArgumentParser()
    argparse.add_argument("file", help="file containing the system")

    args = argparse.parse_args()

    system = parse(args.file)
    system.backward_chaining()
    system.get_solution()


