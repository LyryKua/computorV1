import argparse
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


def main():
    try:
        args = cli_argparse()
        equation = Equation(args.equation.lower().replace(' ', ''))
        exit("exit")
        equation.validate()
        print()
    except IndexError:
        exit('IndexError')
    except Exception as e:
        exit(e)
    # equation = args['equation']
    # print(equation)
    # print(type("tmp"))


if __name__ == '__main__':
    main()
