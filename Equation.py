import re
import math


def get_exp(line):
    return 1 if len(line) == 1 else int(line[2:])


def lst_to_polynomial(lst):
    arr = list()
    for item in lst:
        coef = re.search(r'([+-]|^)(\d*\.)?\d+', item[0])
        coef = coef.group(0) if coef is not None else 1
        exp = re.search(r'x(\^\d+)?', item[0])
        exp = exp.group(0) if exp is not None else 0
        arr.append({
            'coef': float(coef),
            'exp': get_exp(exp) if exp != 0 else exp,
        })
    return arr


class Equation:
    __line = None
    __polynomials = {
        'left': list(),
        'right': list(),
    }
    __monomials = None
    __basis = None
    __root = None

    def __init__(self, line):
        self.__line = line
        equation = line.split('=')
        if len(equation) != 2:
            raise IndexError
        regex = re.compile(
            "(((([+-]|^)(\d*\.)?\d+)((?<=\d)(\*)(?=x))?x?((?<=x)(\^)(?=\d))?((?<=(?<=x)\^)\d+)?)|((([+-]|^)(\d*\.)?\d+)?((?<=\d)(\*)(?=x))?-?x((?<=x)(\^)(?=\d))?((?<=(?<=x)\^)\d+)?))"
        )
        self.__polynomials['left'] = lst_to_polynomial(regex.findall(equation[0]))
        self.__polynomials['right'] = lst_to_polynomial(regex.findall(equation[1]))
        self.__basis = None
        self.__root = None
        self.__d = 0
        self.__polynomial_degree = -1

    def create_basis(self):
        max_exp = -1
        for monomial in self.__monomials:
            max_exp = monomial['exp'] if max_exp < monomial['exp'] else max_exp
        basis = list()
        for index in range(0, max_exp + 1):
            basis.append({
                'coef': 0,
                'exp': index,
            })
        return basis

    def to_left(self):
        rtl = list()
        for polynomial in self.__polynomials['right']:
            rtl.append({
                'coef': -polynomial['coef'],
                'exp': polynomial['exp'],
            })
        return rtl

    def normalize(self):
        self.__monomials = self.__polynomials['left'] + self.to_left()
        self.__basis = self.create_basis()
        for monomial in self.__monomials:
            self.__basis[monomial['exp']]['coef'] += monomial['coef']
        for monomial in self.__basis:
            if monomial['coef'] != 0 and self.__polynomial_degree < monomial['exp']:
                self.__polynomial_degree = monomial['exp']

    def validate(self):
        for i in range(len(self.__basis) - 1, 1, -1):
            if self.__basis[i]['coef'] != 0.0 and self.__basis[i]['exp'] > 2:
                self.print_reduce()
                print("Polynomial degree: {}".format(self.__polynomial_degree))
                raise ValueError('The polynomial degree is strictly greater than 2, I can\'t solve.')

    def imaginary_roots(self):
        a2 = 2 * self.__basis[2]['coef']
        real = (-self.__basis[1]['coef']) / a2
        imaginary = math.fabs(math.sqrt(-self.d) / a2)
        return {
            'x1': '{:.3g} + {:.3g}*i'.format(real, imaginary),
            'x2': '{:.3g} - {:.3g}*i'.format(real, imaginary)
        }

    def solve_square_equation(self):
        self.__d = self.__basis[1]['coef'] * self.__basis[1]['coef'] - 4 * self.__basis[2]['coef'] * self.__basis[0][
            'coef']
        if self.__d < 0:
            self.__root = self.imaginary_roots()
        else:
            self.__root = {
                'x1': '{:.3g}'.format((-self.__basis[1]['coef'] + math.sqrt(self.__d)) / (2 * self.__basis[2]['coef'])),
                'x2': '{:.3g}'.format((-self.__basis[1]['coef'] - math.sqrt(self.__d)) / (2 * self.__basis[2]['coef'])),
            }

    def solve_linear_equation(self):
        self.__root = {
            'x1': '{:.3g}'.format(-self.__basis[0]['coef'] / self.__basis[1]['coef'])
        }

    def solve(self):
        for i in range(len(self.__basis) - 1, 1, -1):
            if self.__basis[i]['coef'] != 0.0 and self.__basis[i]['exp'] > 2:
                raise Exception('exp grater than 2')
        if self.__basis[1]['coef'] != 0.0 and self.__basis[1]['exp'] == 1:
            self.solve_linear_equation()
        elif self.__basis[2]['coef'] != 0.0 and self.__basis[2]['exp'] == 2:
            self.solve_square_equation()
        else:
            print(self.__basis)
            raise Exception("Smth went wrong")

    def print_reduce(self):
        print("Reduced form: ", end="")
        for monomial in self.__basis:
            if monomial['exp'] == 0:
                if monomial['coef'] != 0:
                    print("%.3g*x^%d" % (monomial['coef'], monomial['exp']), end="")
            else:
                if monomial['coef'] != 0:
                    print(" {} ".format('-' if monomial['coef'] < 0 else '+'), end="")
                    print("%.3g*x^%d" % (math.fabs(monomial['coef']), monomial['exp']), end="")
        print(" = 0")

    def print_answer(self):
        self.print_reduce()
        print("Polynomial degree: {}".format(self.__polynomial_degree))

        if self.__d > 0:
            print("Discriminant is strictly positive, the two solutions are:")
        elif self.__d < 0:
            print("Discriminant is strictly negative, roots are imaginary numbers:")
        for key, root in self.__root.items():
            print(root)

    def get_root(self):
        return self.__root
