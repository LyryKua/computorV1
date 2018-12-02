
import re
from pprint import pprint


def get_exponent(line):
    if len(line) == 1:
        return 1
    else:
        return int(line[2:])


def lst_to_polynomial(lst):
    print(lst)
    arr = []
    for item in lst:
        coefficient = re.search(r'([+-]|^)(\d*\.)?\d+', item[0])
        coefficient = coefficient.group(0) if coefficient is not None else 1
        exponent = re.search(r'x(\^\d+)?', item[0])
        exponent = exponent.group(0) if exponent is not None else 0
        arr.append({
            'coefficient': float(coefficient),
            'exponent': get_exponent(exponent) if exponent != 0 else exponent,
        })
    print()
    return arr


class Equation:
    p = {
        'left': [
            {
                'coefficient': 2,
                'exponent': 2,
            },
            {
                'coefficient': -10,
                'exponent': 1,
            },
            {
                'coefficient': 0,
                'exponent': 0,
            },
        ],
        'right': [
            {
                'coefficient': 1,
                'exponent': 2,
            },
            {
                'coefficient': 2,
                'exponent': 1,
            },
            {
                'coefficient': -4,
                'exponent': 0,
            },
        ],
    }

    m = [
            {
                'coefficient': 1,
                'exponent': 2,
            },
            {
                'coefficient': -8,
                'exponent': 1,
            },
            {
                'coefficient': 4,
                'exponent': 0,
            },
        ],

    __polynomials = {
        'left': [],
        'right': [],
    }
    __monomials = None
    __polynomial_degree = None
    __line = None

    def __init__(self, line):
        self.__line = line
        equation = line.split('=')
        if len(equation) != 2:
            raise IndexError
        regex = re.compile(
            "(((([+-]|^)(\d*\.)?\d+)((?<=\d)(\*)(?=x))?x?((?<=x)(\^)(?=\d))?((?<=(?<=x)\^)\d+)?)|((([+-]|^)(\d*\.)?\d+)?((?<=\d)(\*)(?=x))?-?x((?<=x)(\^)(?=\d))?((?<=(?<=x)\^)\d+)?))")
        self.__polynomials['left'] = lst_to_polynomial(regex.findall(equation[0]))
        self.__polynomials['right'] = lst_to_polynomial(regex.findall(equation[1]))
        pprint(self.__polynomials)

    def validate(self):
        pass

    def normalize(self):
        pass
