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


def validate_line(line):
    tmp = re.search(r'(^[\d*^\-+X=x]*$)', line)
    return tmp is not None


def main():
    try:
        args = cli_argparse()
        line = args.equation.lower().replace(' ', '')
        if validate_line(line):
            equation = Equation(line)
            equation.normalize()
            equation.validate()
            equation.solve()
            equation.print_answer()
        else:
            print('forbidden character(s)')
    except IndexError:
        exit('IndexError')
    except ValueError as e:
        exit(e)
    except Exception as e:
        exit(e)


if __name__ == '__main__':
    main()
