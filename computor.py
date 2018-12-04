import argparse
import re
from Equation import Equation


def cli_argparse():
    parser = argparse.ArgumentParser()
    parser.add_argument('-g', '--graph',
                        action='store_true',
                        help='Show graph of equation'
                        )
    parser.add_argument('-s', '--steps',
                        action='store_true',
                        help='Show steps for solution of equation'
                        )
    parser.add_argument('equation',
                        type=str,
                        help='An equation to be solved'
                        )
    return parser.parse_args()


def is_valid_line(line):
    tmp = re.search(r"^[-.*^+x\d]*=[-*^+x\d]*$", line)
    return tmp is not None


def main():
    # try:
        args = cli_argparse()
        line = args.equation.lower().replace(' ', '')
        if is_valid_line(line):
            equation = Equation(line)
            equation.create_basis()
            equation.solve()
            if args.steps:
                equation.print_steps()
            else:
                equation.print_answer()
            if args.graph:
                equation.draw_graph()
            # equation.print_answer()
        else:
            print('forbidden character(s)')
    # except Exception as e:
        # print(dir(e))
        # exit(e)


if __name__ == '__main__':
    main()
