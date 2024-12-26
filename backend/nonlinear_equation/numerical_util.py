from decimal import Decimal
from math import floor, log10

from sympy import symbols, diff, lambdify, sympify, Mul

TOLERANCE = 1e-9

def get_value_on_root(f, *args):
    for arg in args:
        if f(arg) == 0:
            return arg

    return None


def calculate_relative_percent_approximate_error(i, x):
    return abs((x[i] - x[i - 1]) / x[i]) * 100 if i > 0 and x[i] != 0 else float('inf')


def symbolic_derivative(f, order):
    x = symbols('x')
    f_derivative = f(x)
    for _ in range(order):
        f_derivative = diff(f_derivative, x)
    return lambdify(x, f_derivative)


def floating_point_operation(value, sf):
    return round_to_n_significant_figures(float(value), sf) if sf else float(value)


def round_to_n_significant_figures(value, n):
    return 0.0 if not value else round(value, -int(floor(log10(abs(value)))) + (n - 1))


def count_significant_figures(value):
    value = str(value)
    return len(Decimal(value).normalize().as_tuple().digits)


def string_to_lambda(func_str):
    x = symbols('x')
    func_expr = sympify(func_str)
    func_lambda = lambdify(x, func_expr, "sympy")
    return func_lambda


def sign(x):
    if isinstance(x, Mul): return float('NaN') # Even root.
    if isinstance(x, complex):
        if abs(x.real) < TOLERANCE:
            return float('NaN') # Even root.
        else:
            return -1
    else:
        if x > 0: return 1
        elif x < 0: return -1
        else: return 0