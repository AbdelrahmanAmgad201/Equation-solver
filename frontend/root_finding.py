from enum import Enum

from .numerical_util import *

class Status(Enum):
    """
    Enum to represent the status of root-finding methods.
    """
    OK = 0
    INVALID_BRACKET = 1
    TOLERANCE_NOT_REACHED = 2
    SUBTRACTIVE_CANCELLATION = 3
    ZERO_FIRST_DERIVATIVE = 4
    DIVERGE = 5


def bisection(f, xl, xu, es, sf, imax):
    """
    Perform the bisection method to find the root of a function.

    :param f: The function for which the root is to be found.
    :param xl: The lower bound of the bracket.
    :param xu: The upper bound of the bracket.
    :param es: Desired tolerance for the absolute relative approximate error (percentage).
    :param sf: Desired number of significant figures.
    :param imax: Maximum number of iterations to perform.
    :return: A tuple containing:
        - A list of all root estimates from each iteration.
        - A list of all absolute relative approximate errors (in percentage).
        - The number of iterations performed.
        - Status code indicating the result of the computation.
    """


    xr = get_value_on_root(f, xl, xu)
    if xr:
        return [xr], [0], 0, Status.OK

    if f(xl) * f(xu) > 0:
        print("Error: function has the same sign at its end points.")
        return [], [], 0, Status.INVALID_BRACKET

    x = []
    ea = []
    i = 0

    for i in range(imax):
        x.append(floating_point_operation((xl + xu) / 2, sf))

        ea.append(calculate_relative_percent_approximate_error(i, x))
        if ea[i] < es: break

        test = f(xu) * f(x[i])
        if test < 0:
            xl = x[i]
        else:
            xu = x[i]

        if test == 0:
            ea[i] = 0

    return x, ea, i + 1, Status.OK if ea[i] < es else Status.TOLERANCE_NOT_REACHED


def false_position(f, xl, xu, es, sf, imax):
    """
    Perform the false position (regula falsi) method to find the root of a function.

    :param f: The function for which the root is to be found.
    :param xl: The lower bound of the bracket.
    :param xu: The upper bound of the bracket.
    :param es: Desired tolerance for the absolute relative approximate error (percentage).
    :param sf: Desired number of significant figures.
    :param imax: Maximum number of iterations to perform.
    :return: A tuple containing:
        - A list of all root estimates from each iteration.
        - A list of all absolute relative approximate errors (in percentage).
        - The number of iterations performed.
        - Status code indicating the result of the computation.
    """

    xr = get_value_on_root(f, xl, xu)
    if xr:
        return [xr], [0], 0, Status.OK

    if f(xl) * f(xu) > 0:
        print("Error: function has the same sign at its end points.")
        return [], [], 0, Status.INVALID_BRACKET

    x = []
    ea = []
    i = 0

    for i in range(imax):
        fu = f(xu)
        fl = f(xl)

        if (fu - fl) == 0:
            print("Error: subtractive cancellation in the denominator (fu - fl = 0).")
            return x, ea, i + 1, Status.SUBTRACTIVE_CANCELLATION

        x.append(floating_point_operation((xl * fu - xu * fl) / (fu - fl), sf))
        fr = f(x[i])

        ea.append(calculate_relative_percent_approximate_error(i, x))
        if ea[i] < es: break

        if fr == 0:
            break

        if fr * fl < 0:
            xu = x[i]
        else:
            xl = x[i]

    return x, ea, i + 1, Status.OK if ea[i] < es else Status.TOLERANCE_NOT_REACHED


def fixed_point(g, x0, es, sf, imax):
    """
    Perform the fixed-point iteration method to find the root of a function.

    :param g: Function g(x) for the fixed-point iteration.
    :param x0: Initial guess for the root.
    :param es: Desired tolerance for the absolute relative approximate error (percentage).
    :param sf: Desired number of significant figures.
    :param imax: Maximum number of iterations to perform.
    :return: A tuple containing:
        - A list of root estimates for each iteration.
        - A list of all absolute relative approximate errors (in percentage).
        - The number of iterations performed.
        - Status code indicating the result of the computation.
    """

    x = [x0]
    ea = [float('inf')]
    i = 0

    for i in range(imax):

        try:
            x.append(floating_point_operation(g(x[i]), sf))
        except OverflowError as _:
            return x, ea, i + 1, Status.DIVERGE

        ea.append(calculate_relative_percent_approximate_error(i + 1, x))
        if ea[i] < es: break

    return x, ea, i + 1, Status.OK if ea[i] < es else Status.TOLERANCE_NOT_REACHED


def newton_raphson(f, x0, es, sf, imax):
    """
    Perform the Newton-Raphson method to find the root of a function.

    :param f: The function for which the root is to be found.
    :param x0: Initial guess for the root.
    :param es: Desired tolerance for the absolute relative approximate error (percentage).
    :param sf: Desired number of significant figures.
    :param imax: Maximum number of iterations to perform.
    :return: A tuple containing:
        - A list of root estimates for each iteration.
        - A list of all absolute relative approximate errors (in percentage).
        - The number of iterations performed.
        - Status code indicating the result of the computation.
    """

    xr = get_value_on_root(f, x0)
    if xr:
        return [xr], [0], 0, Status.OK

    f_prime = symbolic_derivative(f, 1)

    x = [x0]
    i = 0
    ea = [float('inf')]

    for i in range(imax):
        f_prime_xi = evaluate_symbolic_expression(f_prime, x[i])
        if f_prime_xi == 0:
            print("Error: derivative of f(x) = 0.")
            return x, ea, i + 1, Status.ZERO_FIRST_DERIVATIVE

        x.append(floating_point_operation(x[i] - f(x[i]) / f_prime_xi, sf))

        ea.append(calculate_relative_percent_approximate_error(i + 1, x))
        if ea[i] < es: break

    return x, ea, i + 1, Status.OK if ea[i] < es else Status.TOLERANCE_NOT_REACHED


def first_modified_newton_raphson(f, x0, m, es, sf, imax):
    """
    Perform the first modified Newton-Raphson method to find the root of a function.

    :param f: The function for which the root is to be found.
    :param x0: Initial guess for the root.
    :param m: Multiplicity of the root.
    :param es: Desired tolerance for the absolute relative approximate error (percentage).
    :param sf: Desired number of significant figures.
    :param imax: Maximum number of iterations to perform.
    :return: A tuple containing:
        - A list of all root estimates from each iteration.
        - A list of all absolute relative approximate errors (in percentage).
        - The number of iterations performed.
        - Status code indicating the result of the computation.
    """

    xr = get_value_on_root(f, x0)
    if xr:
        return [xr], [0], 0, Status.OK

    f_prime = symbolic_derivative(f, 1)

    x = [x0]
    i = 0
    ea = [float('inf')]

    for i in range(imax):
        f_prime_xi = evaluate_symbolic_expression(f_prime, x[i])
        if f_prime_xi == 0:
            print("Error: derivative of f(x) = 0.")
            return x, ea, i + 1, Status.ZERO_FIRST_DERIVATIVE

        x.append(floating_point_operation(x[i] - m * f(x[i]) / f_prime_xi, sf))

        ea.append(calculate_relative_percent_approximate_error(i + 1, x))
        if ea[i] < es: break

    return x, ea, i + 1, Status.OK if ea[i] < es else Status.TOLERANCE_NOT_REACHED


def second_modified_newton_raphson(f, x0, es, sf, imax):
    """
    Perform the second modified Newton-Raphson method to find the root of a function.

    :param f: The function for which the root is to be found.
    :param x0: Initial guess for the root.
    :param es: Desired tolerance for the absolute relative approximate error (percentage).
    :param sf: Desired number of significant figures.
    :param imax: Maximum number of iterations to perform.
    :return: A tuple containing:
        - A list of all root estimates from each iteration.
        - A list of all absolute relative approximate errors (in percentage).
        - The number of iterations performed.
        - Status code indicating the result of the computation.
    """

    xr = get_value_on_root(f, x0)
    if xr:
        return [xr], [0], 0, Status.OK

    f_prime = symbolic_derivative(f, 1)
    f_double_prime = symbolic_derivative(f, 2)

    x = [x0]
    i = 0
    ea = [float('inf')]

    for i in range(imax):

        f_xi = f(x[i])
        f_prime_xi = evaluate_symbolic_expression(f_prime, x[i])
        f_double_prime_xi = evaluate_symbolic_expression(f_double_prime, x[i])

        if f_prime_xi ** 2 - f_xi * f_double_prime_xi == 0:
            print("Error: subtractive cancellation in the denominator (f'(x)^2 - f(x) * f''(x) = 0).")
            return x, ea, i + 1, Status.SUBTRACTIVE_CANCELLATION

        x.append(floating_point_operation(x[i] - (f_xi * f_prime_xi) / (f_prime_xi ** 2 - f_xi * f_double_prime_xi), sf))

        ea.append(calculate_relative_percent_approximate_error(i + 1, x))
        if ea[i] < es: break

    return x, ea, i + 1, Status.OK if ea[i] < es else Status.TOLERANCE_NOT_REACHED


def secant(f, x0, x1, es, sf, imax):
    """
    Perform the secant method to find the root of a function.

    :param f: The function for which the root is to be found.
    :param x0: Initial guess for the root.
    :param x1: Second initial guess for the root.
    :param es: Desired tolerance for the absolute relative approximate error (percentage).
    :param sf: Desired number of significant figures.
    :param imax: Maximum number of iterations to perform.
    :return: A tuple containing:
        - A list of all root estimates from each iteration.
        - A list of all absolute relative approximate errors (in percentage).
        - The number of iterations performed.
        - Status code indicating the result of the computation.
    """

    xr = get_value_on_root(f, x0, x1)
    if xr:
        return [xr], [0], 0, Status.OK

    x = [x0, x1]
    ea = [float('inf'), float('inf') if x1 == 0 else abs((x1 - x0) / x1)]
    i = 1

    for i in range(1, imax):
        f_i_1 = f(x[i - 1])
        f_i = f(x[i])

        if f_i_1 - f_i == 0:
            print("Error: subtractive cancellation in the denominator (f_i-1 - f_i = 0).")
            return x, ea, i + 1, Status.SUBTRACTIVE_CANCELLATION

        x.append(floating_point_operation(x[i] - (f_i * (x[i - 1] - x[i])) / (f_i_1 - f_i), sf))

        ea.append(calculate_relative_percent_approximate_error(i, x))
        if ea[i] < es: break

    return x, ea, i + 1, Status.OK if ea[i] < es else Status.TOLERANCE_NOT_REACHED