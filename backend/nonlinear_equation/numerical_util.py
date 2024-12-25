from decimal import Decimal

from sympy import symbols, diff

from math import floor, log10


def get_value_on_root(f, *args):
    for arg in args:
        if f(arg) == 0:
            return arg

    return None

def calculate_relative_percent_approximate_error(i, x):
    return abs((x[i] - x[i - 1]) / x[i]) * 100 if i > 0 and x[i] != 0 else float('inf')


def symbolic_derivative(f, order):
    """
    Compute the symbolic derivative of a given function to a specified order.

    :param f: Function for which the derivative is to be calculated.
    :param order: Order of the derivative.
    :return: Symbolic expression for the derivative.
    """

    x = symbols('x')
    f_derivative = f(x)
    for _ in range(order):
        f_derivative = diff(f_derivative, x)
    return f_derivative


def evaluate_symbolic_expression(symbolic_expression, x0):
    """
    Evaluate a symbolic expression at a given point.

    :param symbolic_expression: The symbolic expression to evaluate.
    :param x0: The point at which to evaluate the expression.
    :return: The numerical result of the evaluation.
    """

    x = symbols('x')
    return symbolic_expression.evalf(subs={x: x0})

def floating_point_operation(value, sf):
    return round_to_n_significant_figures(value, sf) if sf else value

def count_significant_figures(value):
    value = str(value)
    return len(Decimal(value).normalize().as_tuple().digits)

def round_to_n_significant_figures(value, n):
    return value if value == 0 else round(value, -int(floor(log10(abs(value)))) + (n - 1))