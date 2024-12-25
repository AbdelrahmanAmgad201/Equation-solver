from math import log10
from time import time

from .numerical_util import count_significant_figures
from .root_find import (bisection,
                       false_position,
                       fixed_point,
                       newton_raphson,
                       secant,
                       first_modified_newton_raphson,
                       second_modified_newton_raphson,
                       Status)

status_messages = {
    Status.INVALID_BRACKET: "Function has the same sign at its end points.",
    Status.ZERO_FIRST_DERIVATIVE: "First derivative of f(x) = 0.",
    Status.SUBTRACTIVE_CANCELLATION: "Subtractive cancellation in the denominator.",
    Status.DIVERGE: "The method has diverged.",
    Status.TOLERANCE_NOT_REACHED: "The desired tolerance was not achieved.",
    Status.OK: ""
}

methods = {
    "Bisection": bisection,
    "False-Position": false_position,
    "Fixed point": fixed_point,
    "Original Newton-Raphson": newton_raphson,
    "First Modified Newton-Raphson": first_modified_newton_raphson,
    "Second Modified Newton-Raphson": second_modified_newton_raphson,
    "Secant": secant
}


class Solver:
    def __init__(self):
        self.final_result = {'time': time(),
                             'root': "",
                             'iterations': "",
                             'relative_error': "",
                             'significant_figures': "",
                             'error_msg': "",
                             "method": ""}
        self.steps = []

    def solve(self, data):
        args = {'f': data['equation'],
                'es': data['tolerance'],
                'sf': data['significant_figures'],
                'imax': data['max_itr']}

        self.final_result['time'] = time()
        self.final_result['time'] = time() - self.final_result['time']
        method = data['method']
        match method:
            case "Bisection" | "False-Position":
                args['xl'] = data['low_bound']
                args['xu'] = data['high_bound']

            case "Fixed point" | "Original Newton-Raphson" | "First Modified Newton-Raphson" | "Second Modified Newton-Raphson":
                args['x0'] = data['initial_guess']
                match method:
                    case "Fixed point":
                        args['g'] = data['gx_equation']
                    case "First Modified Newton-Raphson":
                        args['m'] = data['multiplicity']

            case "Secant":
                args['x0'] = data['secant_p1']
                args['x1'] = data['secant_p2']

        # Invoke the chosen method
        self.final_result['time'] = time()
        x, ea, it, status = methods[method](**args)
        self.final_result['time'] = time() - self.final_result['time']

        # Get number of iterations and status
        self.final_result.update({
            'iterations': format_number(it),
            'error_msg': status_messages[status],
        })

        # Get the root
        if len(x) > 0:
            self.final_result['root'] = "0" if x[-1] == 0 else format_number(x[-1])
        else:
            self.final_result['root'] = "—"

        # Get the number of correct significant figures abd the absolute approximate relative error
        if len(ea) > 0:
            if ea[-1] == float('inf'):
                self.final_result['relative_error'] = "Infinity"
                self.final_result['significant_figures'] = "—"
            else:
                self.final_result['relative_error'] = format_number(ea[-1])
                if ea[-1] == 0:
                    self.final_result['significant_figures'] = format_number(count_significant_figures(ea[-1]))
                else:
                    self.final_result['significant_figures'] = format_number(int(2 - log10(2 * ea[-1])))
        else:
            self.final_result['relative_error'] = "—"
            self.final_result['significant_figures'] = "—"

        self.steps = [{'xr': format_number(xr_value), 'ea': format_number(ea_value)}
                      for xr_value, ea_value in zip(x, ea)]
        return self.final_result, self.steps


def format_number(value):
    return str(int(value)) if float(value).is_integer() else str(value)
