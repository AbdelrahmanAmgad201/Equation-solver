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
    COMPLEX = 6



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

    # Check if xl or xu are valid roots
    xr = get_value_on_root(f, xl, xu)
    if xr is not None:
        return [xr], [0], 0, Status.OK

    if f(xl) * f(xu) > 0:
        print("Error: function has the same sign at its end points.")
        return [], [], 0, Status.INVALID_BRACKET

    x = []
    ea = []
    i = 0

    for i in range(imax):
        x.append(floating_point_operation((xl + xu) / 2, sf))

        test = f(xu) * f(x[i])
        if test < 0:
            xl = x[i]
        elif test > 0:
            xu = x[i]
        else:
            ea.append(0)
            break

        ea.append(calculate_relative_percent_approximate_error(i, x))
        if ea[i] < es: break

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

    # Check if xl or xu are valid roots
    xr = get_value_on_root(f, xl, xu)
    if xr is not None:
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
            return x, ea, i, Status.SUBTRACTIVE_CANCELLATION

        x.append(floating_point_operation((xl * fu - xu * fl) / (fu - fl), sf))
        fr = f(x[i])

        if fr * fl < 0:
            xu = x[i]
        elif fr * fl > 0:
            xl = x[i]
        else:
            ea.append(0)
            break

        ea.append(calculate_relative_percent_approximate_error(i, x))
        if ea[i] < es: break

    return x, ea, i + 1, Status.OK if ea[i] < es else Status.TOLERANCE_NOT_REACHED


def fixed_point(f, g, x0, es, sf, imax):
    """
    Perform the fixed-point iteration method to find the root of a function.

    :param f: The function for which the root is to be found.
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

    # Check if x0 is a valid root
    xr = get_value_on_root(f, x0)
    if xr is not None:
        return [xr], [0], 0, Status.OK

    x = [x0]
    ea = [float('inf')]
    i = 0

    for i in range(imax):

        # Check for divergence (overflow)
        try:
            xr = g(x[i])

            if isinstance(xr, complex):
                return x, ea, i, Status.COMPLEX

            x.append(floating_point_operation(xr, sf))

            if f(x[i + 1]) == 0:
                ea.append(0)
                break

        except OverflowError as _:
            return x, ea, i, Status.DIVERGE

        ea.append(calculate_relative_percent_approximate_error(i + 1, x))
        if ea[i + 1] < es: break

    return x, ea, i + 1, Status.OK if ea[i + 1] < es else Status.DIVERGE


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
    if xr is not None:
        return [xr], [0], 0, Status.OK

    f_prime = symbolic_derivative(f, 1)

    x = [x0]
    i = 0
    ea = [float('inf')]

    for i in range(imax):
        f_prime_xi = f_prime(x[i])
        if f_prime_xi == 0:
            print("Error: derivative of f(x) = 0.")
            return x, ea, i, Status.ZERO_FIRST_DERIVATIVE

        x.append(floating_point_operation(x[i] - f(x[i]) / f_prime_xi, sf))

        if f(x[i + 1]) == 0:
            ea.append(0)
            break

        ea.append(calculate_relative_percent_approximate_error(i + 1, x))
        if ea[i + 1] < es: break

    return x, ea, i + 1, Status.OK if ea[i + 1] < es else Status.DIVERGE


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
    if xr is not None:
        return [xr], [0], 0, Status.OK

    f_prime = symbolic_derivative(f, 1)

    x = [x0]
    i = 0
    ea = [float('inf')]

    for i in range(imax):
        f_prime_xi = f_prime(x[i])
        if f_prime_xi == 0:
            print("Error: derivative of f(x) = 0.")
            return x, ea, i, Status.ZERO_FIRST_DERIVATIVE

        x.append(floating_point_operation(x[i] - m * f(x[i]) / f_prime_xi, sf))

        if f(x[i + 1]) == 0:
            ea.append(0)
            break

        ea.append(calculate_relative_percent_approximate_error(i + 1, x))
        if ea[i + 1] < es: break

    return x, ea, i + 1, Status.OK if ea[i + 1] < es else Status.DIVERGE


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
    if xr is not None:
        return [xr], [0], 0, Status.OK

    f_prime = symbolic_derivative(f, 1)
    f_double_prime = symbolic_derivative(f, 2)

    x = [x0]
    i = 0
    ea = [float('inf')]

    for i in range(imax):

        f_xi = f(x[i])
        f_prime_xi = f_prime(x[i])
        f_double_prime_xi = f_double_prime(x[i])

        if f_prime_xi ** 2 - f_xi * f_double_prime_xi == 0:
            print("Error: subtractive cancellation in the denominator (f'(x)^2 - f(x) * f''(x) = 0).")
            return x, ea, i, Status.SUBTRACTIVE_CANCELLATION

        x.append(floating_point_operation(x[i] - (f_xi * f_prime_xi) / (f_prime_xi ** 2 - f_xi * f_double_prime_xi), sf))

        if f(x[i + 1]) == 0:
            ea.append(0)
            break

        ea.append(calculate_relative_percent_approximate_error(i + 1, x))
        if ea[i + 1] < es: break

    return x, ea, i + 1, Status.OK if ea[i + 1] < es else Status.DIVERGE


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
    if xr is not None:
        return [xr], [0], 0, Status.OK

    x = [x0, x1]
    ea = [float('inf'), float('inf')]
    i = 1

    for i in range(1, imax):
        f_i_1 = f(x[i - 1])
        f_i = f(x[i])

        if f_i_1 - f_i == 0:
            print("Error: subtractive cancellation in the denominator (f_i-1 - f_i = 0).")
            return x, ea, i, Status.SUBTRACTIVE_CANCELLATION

        x.append(floating_point_operation(x[i] - (f_i * (x[i - 1] - x[i])) / (f_i_1 - f_i), sf))

        if f(x[i + 1]) == 0:
            ea.append(0)
            break

        ea.append(calculate_relative_percent_approximate_error(i, x))
        if ea[i + 1] < es: break

    return x, ea, i + 1, Status.OK if ea[i + 1] < es else Status.DIVERGE