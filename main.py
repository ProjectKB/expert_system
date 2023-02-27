import argparse as a

from src.parse import parse


if __name__ == '__main__':
    argparse = a.ArgumentParser()
    argparse.add_argument("file", help="file containing the system")
    argparse.add_argument("-s", "--system", action="store_true", default=False, help="show system")
    argparse.add_argument("-g", "--graph", action="store_true", default=False, help="show graph")
    argparse.add_argument("-i", "--interactive", action="store_true", default=False, help="show graph")

    args = argparse.parse_args()
    system = parse(args.file)

    if args.system:
        print(system)
    if args.graph:
        system.show_graph()

    system.backward_chaining()

    if args.interactive:
        system.handle_interactive()
