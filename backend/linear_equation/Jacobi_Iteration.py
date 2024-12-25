import numpy as np
import math


class Jacobi_iteration:

    def __init__(self, parser, error=None, iterations=None, sf=5, initial=None):
        self._all_iterations =[]

        self.matrixA = np.array(parser.get_matrixA(), dtype=float)
        self.matrixB = np.array(parser.get_matrixB(), dtype=float)
        self.error = None if error == '' else float(error)
        self.iterations = None if iterations == '' else int(iterations)
        self.initial = np.array(initial, dtype=float)
        self.sf = int(sf)
        self.numbers = self.initial.copy()



    def solve(self):
        print("helloo "+str(self.error)+ " "+ str(self.iterations))
        if self.error is not None:
            return self._solve_numerical_error()
        if self.iterations is not None:
            return self._solve_numerical_iterations()

    def _solve_numerical_error(self):
        newnumbers = self.initial.copy()

        max_iterations = 1000
        iteration_count = 0
        while True:
            old_numbers = newnumbers.copy()
            self._all_iterations.append(old_numbers)
            for i in range(len(self.matrixA)):
                sum_val = np.dot(self.matrixA[i, :], old_numbers) - self.matrixA[i, i] * old_numbers[i]
                newnumbers[i] = (self.matrixB[i] - sum_val) / self.matrixA[i, i]
                newnumbers[i] = self.round_significant(newnumbers[i], self.sf)

            error_current = np.linalg.norm(newnumbers - old_numbers) / np.linalg.norm(newnumbers)
            iteration_count += 1
            if error_current < self.error or iteration_count >= max_iterations:
                break
        return self._all_iterations

    def _solve_numerical_iterations(self):

        while self.iterations:
            old_numbers = self.numbers.copy()
            self._all_iterations.append(old_numbers)
            for i in range(len(self.matrixA)):
                sum_val = np.dot(self.matrixA[i, :], old_numbers) - self.matrixA[i, i] * self.numbers[i]
                self.numbers[i] = (self.matrixB[i] - sum_val) / self.matrixA[i, i]
                self.numbers[i] = self.round_significant(self.numbers[i], self.sf)
            self.iterations -= 1

        return self._all_iterations

    def round_significant(self, number, sig_figs):
        if number == 0:
            return 0

        scale = math.floor(math.log10(abs(number)))

        factor = 10 ** (int(sig_figs) - scale - 1)


        return round(number * factor) / factor
