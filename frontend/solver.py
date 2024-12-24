import time
import math

class Solver():
    def bisection_method(self):
        final_result = {}
        start_time = time.time()
        final_result["time"] = time.time() - start_time
        final_result["root"] = 2.345
        final_result["iterations"] = 15
        final_result["relative_error"] = 0.0001
        final_result["significant_figures"] = math.floor(-math.log10(0.001))
        final_result["error_msg"] = ""
        steps = [
            {'xl':0, 'xh':2, 'xr':1, 'e':'-'},
            {'xl':0, 'xh':2, 'xr':1, 'e':'-'},
            {'xl':0, 'xh':2, 'xr':1, 'e':'-'},
            {'xl':0, 'xh':2, 'xr':1, 'e':'-'}
        ]
        return (final_result, steps)

    def false_position_method(self):
        pass
    def fixed_point_method(self):
        pass
    def original_newton_raphson_method(self):
        pass
    def modified_newton_raphson_method(self):
        pass
    def secant_method(self):
        pass