import argparse as a

import src.parser as parser


if __name__ == '__main__':
    argparse = a.ArgumentParser()
    argparse.add_argument("file", help="file containing the system")

    args = argparse.parse_args()

    system = parser.parse(args.file)
    print(system)
    # system.show_graph()

