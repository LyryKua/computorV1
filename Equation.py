import re
import math
import matplotlib.pyplot as plt


def get_exp(line):
    return 1 if len(line) == 1 else int(line[2:])


def lst_to_polynomial(lst):
    arr = list()
    for item in lst:
        coef = re.search(r'([+-]|^)(\d*\.)?\d+', item)
        coef = coef.group(0) if coef is not None else 1
        exp = re.search(r'x(\^\d+)?', item)
        exp = exp.group(0) if exp is not None else 0
        arr.append({
            'coef': float(coef),
            'exp': get_exp(exp) if exp != 0 else exp,
        })
    return arr


def line_to_lst(line):
    arr = list()
    for c in line:
        if c == '-' or c == '+' or len(arr) == 0:
            arr.append("")
        arr[len(arr) - 1] += c
    return arr


class Equation:

    def __init__(self, line):

        self.__polynomials = {
            'left': list(),
            'right': list(),
        }
        self.__monomials = list()
        self.__basis = list()
        self.__roots = {
            'x1': '',
            'x2': '',
        }
        self.__line = line
        self.__d = -1
        self.__polynomial_degree = -1

        tmp = self.__line.split('=')
        pol = {
            'left': line_to_lst(tmp[0]),
            'right': line_to_lst(tmp[1])
        }
        self.__validate(pol)
        self.__polynomials['left'] = lst_to_polynomial(pol['left'])
        self.__polynomials['right'] = lst_to_polynomial(pol['right'])

    @staticmethod
    def __validate(pol):
        regex = re.compile(
            "(^[+-]?(\d*\.)?(\d+)?((?<=\d)(\*)(?=x))?((?<=[-+*])x|(?<=^)x)?((?<=x)(\^)(?=\d))?((?<=(?<=x)\^)\d+)?$)"
        )
        for side, polynomial in pol.items():
            for monomial in polynomial:
                if regex.search(monomial) is None:
                    raise Exception("Wrong format!")

    def create_basis(self):
        self.__right_to_left()
        max_exp = -1
        for monomial in self.__monomials:
            max_exp = monomial['exp'] if max_exp < monomial['exp'] else max_exp
        for i in range(0, max_exp + 1):
            self.__basis.append({
                'coef': 0,
                'exp': i,
            })
        for monomial in self.__monomials:
            self.__basis[monomial['exp']]['coef'] += monomial['coef']
        tmp = [x for x in self.__basis if x['coef'] == 0.0 and x['exp'] > 2]
        for item in tmp:
            self.__basis.remove(item)
        if len(self.__basis) == 0:
            print("Reduced form: 0*x^1 = 0")
            self.print_polynomial_degree(1)
            raise Exception("All the real numbers are solution")
        self.__set_polynomial_degree()

    def __set_polynomial_degree(self):
        print(len(self.__basis))
        self.__polynomial_degree = self.__basis[len(self.__basis) - 1]['exp']

    def solve(self):
        if self.__polynomial_degree > 2:
            self.print_reduce()
            self.print_polynomial_degree(self.__polynomial_degree)
            raise Exception('The polynomial degree is strictly greater than 2, I can\'t solve.')
        if self.__polynomial_degree == 2:
            self.solve_square_equation()
        elif self.__polynomial_degree == 1:
            self.solve_linear_equation()
        else:
            print("???")

    def __right_to_left(self):
        self.__monomials = self.__polynomials['left']
        for polynomial in self.__polynomials['right']:
            self.__monomials.append({
                'coef': -polynomial['coef'],
                'exp': polynomial['exp']
            })
        self.__monomials = [x for x in self.__monomials if x['coef'] != 0.0]

    def imaginary_roots(self):
        a2 = 2 * self.__basis[2]['coef']
        real = (-self.__basis[1]['coef']) / a2
        imaginary = math.fabs(math.sqrt(-self.__d) / a2)
        return {
            'x1': '{:.3g} + {:.3g}*i'.format(real, imaginary),
            'x2': '{:.3g} - {:.3g}*i'.format(real, imaginary)
        }

    def solve_square_equation(self):
        self.__d = self.__basis[1]['coef'] * self.__basis[1]['coef'] - 4 * self.__basis[2]['coef'] * self.__basis[0][
            'coef']
        if self.__d < 0:
            self.__roots = self.imaginary_roots()
        else:
            self.__roots = {
                'x1': '{:.3g}'.format((-self.__basis[1]['coef'] + math.sqrt(self.__d)) / (2 * self.__basis[2]['coef'])),
                'x2': '{:.3g}'.format((-self.__basis[1]['coef'] - math.sqrt(self.__d)) / (2 * self.__basis[2]['coef'])),
            }

    def solve_linear_equation(self):
        self.__roots = {
            'x': '{:.3g}'.format(-self.__basis[0]['coef'] / self.__basis[1]['coef'])
        }

    @staticmethod
    def print_polynomial(polynomial):
        for i in range(len(polynomial) - 1, -1, -1):
            monomial = polynomial[i]
            if i == len(polynomial) - 1:
                if monomial['coef'] != 0:
                    print("%.3g*x^%d" % (monomial['coef'], monomial['exp']), end="")
            else:
                if monomial['coef'] != 0:
                    print(" {} ".format('-' if monomial['coef'] < 0 else '+'), end="")
                    print("%.3g*x^%d" % (math.fabs(monomial['coef']), monomial['exp']), end="")
        print(" = 0")

    def print_reduce(self):
        print("Reduced form: ", end="")
        self.print_polynomial(self.__basis)

    @staticmethod
    def print_polynomial_degree(polynomial_degree):
        print("Polynomial degree: {}".format(polynomial_degree))

    def print_answer(self):
        self.print_reduce()
        self.print_polynomial_degree(self.__polynomial_degree)
        print("The solution is:")
        self.print_roots()

    def print_roots(self):
        for key, value in self.__roots.items():
            print("{} = {}".format(key, value))

    def print_steps(self):
        print("Right to left: ", end="")
        self.print_polynomial(self.__monomials)
        self.print_reduce()
        print()
        self.print_polynomial_degree(self.__polynomial_degree)
        print()
        if self.__polynomial_degree == 2:
            print("a = %.3g" % self.__basis[2]['coef'])
            print("b = %.3g" % self.__basis[1]['coef'])
            print("c = %.3g\n" % self.__basis[0]['coef'])
            print("D = b * b - 4 * a * c = {b} * {b} - 4 * {a} * {c} = {d}".format(
                a="%.3g" % self.__basis[2]['coef'],
                b="%.3g" % self.__basis[1]['coef'],
                c="%.3g" % self.__basis[0]['coef'],
                d="%.3g" % self.__d
            ))
            print("\nx12 = (-b ± √D) / (2 * a)")
            for key, value in self.__roots.items():
                print("{key} = (-{b} + √{d}) / (2 * {a}) = {value}".format(
                    key=key,
                    b="%.3g" % self.__basis[1]['coef'],
                    a="%.3g" % self.__basis[2]['coef'],
                    d="%.3g" % self.__d,
                    value=value
                ))
        elif self.__polynomial_degree == 1:
            print("k = %.3g" % self.__basis[1]['coef'])
            print("b = %.3g" % self.__basis[0]['coef'])
            print("\nx = -b / k = {b} / {k} = {x}".format(
                k=-self.__basis[1]['coef'],
                b=self.__basis[0]['coef'],
                x=self.__roots['x']
            ))
        print("\nThe solution is:")
        self.print_roots()

    def draw_graph(self):
        if self.__d >= 0:
            x = range(-100, 100)
            y = list()
            for i in x:
                tmp = 0
                for monomial in self.__basis:
                    tmp += monomial['coef'] * math.pow(i, monomial['exp'])
                y.append(tmp)
            plt.plot(x, y)
            plt.show()
