import numpy as np
import math


class Gauss_Seidel:
    _all_iterations = []

    def __init__(self, parser, error=None, iterations=None, sf=5, initial=None):
        self._all_iterations = []
        self.matrixA = np.array(parser.get_matrixA(), dtype=float)
        self.matrixB = np.array(parser.get_matrixB(), dtype=float)
        self.error = None if error == '' else float(error)
        self.iterations = None if iterations == '' else int(iterations)
        self.initial = np.array(initial, dtype=float)
        self.sf = int(sf)
        self.numbers = self.initial.copy()

    def solve(self):

        if self.error == None:
            return self._solve_numerical_iterations()
        elif self.iterations == None:
            return self._solve_numerical_error()

    def _solve_numerical_error(self):

        while True:
            old_numbers = np.copy(self.initial)
            for i in range(len(self.matrixA)):
                sum_val = np.dot(self.matrixA[i, :], self.initial) - self.matrixA[i, i] * self.initial[i]
                self.initial[i] = (self.matrixB[i] - sum_val) / self.matrixA[i, i]
                self.initial[i] = self.round_significant(self.initial[i], self.sf)
            self._all_iterations.append(np.copy(self.initial))
            error_current= (np.max(np.abs(self.initial - old_numbers) / np.abs(self.initial)))*100
            if error_current < self.error:
                break
        return self._all_iterations
    def _solve_numerical_iterations(self):

        while self.iterations:
            for i in range(len(self.matrixA)):
                sum_val = np.dot(self.matrixA[i, :], self.initial) - self.matrixA[i, i] * self.initial[i]
                self.initial[i] = (self.matrixB[i] - sum_val) / self.matrixA[i, i]
                self.initial[i] = self.round_significant(self.initial[i],self.sf)
            self.iterations -= 1
            self._all_iterations.append(np.copy(self.initial))
        return self._all_iterations

    def round_significant(self, number, sig_figs):
        if number == 0:
            return 0
        scale = math.floor(math.log10(abs(number)))
        factor = 10 ** (sig_figs - scale - 1)
        return round(number * factor) / factor