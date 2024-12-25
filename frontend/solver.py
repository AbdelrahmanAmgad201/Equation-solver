from .numerical_util import count_significant_figures

from math import log10

from time import time

from .root_finding import (bisection,
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
    Status.TOLERANCE_NOT_REACHED: "The desired tolerance was not achieved.",
    Status.DIVERGE: "The method has diverged.",
    Status.OK: ""
}

class Solver:

    def __init__(self):
        self.final_result = {'time': time(),
                             'root': 0.0,
                             'iterations': 0,
                             'relative_error': 0.0,
                             'significant_figures': 0,
                             'error_msg': "",
                             "method": ""}
        self.steps = []


    def solve(self, data):
        x, ea, it, status = None, None, None, None
        match data['method']:
            case "Bisection":
                self.final_result['time'] = time()
                x, ea, it, status = bisection(data['equation'],
                                              data['low_bound'],
                                              data['high_bound'],
                                              data['tolerance'],
                                              data['significant_figures'],
                                              data['max_itr'])
                self.final_result['time'] = time() - self.final_result['time']
            case "False-Position":
                self.final_result['time'] = time()
                x, ea, it, status = false_position(data['equation'],
                                              data['low_bound'],
                                              data['high_bound'],
                                              data['tolerance'],
                                              data['significant_figures'],
                                              data['max_itr'])
                self.final_result['time'] = time() - self.final_result['time']
            case "Fixed point":
                self.final_result['time'] = time()
                x, ea, it, status = fixed_point(data['gx_equation'],
                                                data['initial_guess'],
                                                data['tolerance'],
                                                data['significant_figures'],
                                                data['max_itr'])
                self.final_result['time'] = time() - self.final_result['time']
            case "Original Newton-Raphson":
                self.final_result['time'] = time()
                x, ea, it, status = newton_raphson(data['equation'],
                                                data['initial_guess'],
                                                data['tolerance'],
                                                data['significant_figures'],
                                                data['max_itr'])
                self.final_result['time'] = time() - self.final_result['time']
            case "First Modified Newton-Raphson":
                self.final_result['time'] = time()
                x, ea, it, status = first_modified_newton_raphson(data['equation'],
                                                                  data['initial_guess'],
                                                                  data['multiplicity'],
                                                                  data['tolerance'],
                                                                  data['significant_figures'],
                                                                  data['max_itr'])
                self.final_result['time'] = time() - self.final_result['time']
            case "Second Modified Newton-Raphson":
                self.final_result['time'] = time()
                x, ea, it, status = second_modified_newton_raphson(data['equation'],
                                                                   data['initial_guess'],
                                                                   data['tolerance'],
                                                                   data['significant_figures'],
                                                                   data['max_itr'])
                self.final_result['time'] = time() - self.final_result['time']
            case "Secant":
                self.final_result['time'] = time()
                x, ea, it, status = secant(data['equation'],
                                           data['secant_p1'],
                                           data['secant_p2'],
                                           data['tolerance'],
                                           data['significant_figures'],
                                           data['max_itr'])
                self.final_result['time'] = time() - self.final_result['time']
        self.final_result.update({
            'root': x[-1] if len(x) > 0 else "—",
            'relative_error': ea[-1] if len(ea) > 0 else "—",
            'iterations': it,
            'error_msg': status_messages[status],
            'significant_figures': (count_significant_figures(ea[-1]) if ea[-1] == 0 else int(2 - log10(2 * ea[-1]))) if len(ea) > 0 else 0,
        })
        self.steps = [{'xr': xr_value, 'ea': ea_value} for xr_value, ea_value in zip(x, ea)]
        return self.final_result, self.steps