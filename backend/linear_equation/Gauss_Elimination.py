from .parser import Parser
import sympy as sp
import math


class Gauss_Elimination:
    _solution_line = []

    def __init__(self, parser):
        self._solution_line = []
        self.matrixA = parser.get_matrixA()
        self.matrixB = parser.get_matrixB()

    def solve(self, sf):
        sf = int(sf)  # Ensure sf is an integer

        # Helper function to round elements to significant figures
        def round_sf(value, sig_figs):
            if value == 0:
                return 0
            elif isinstance(value, sp.Basic):  # For SymPy symbolic objects
                return value.evalf(sig_figs)
            else:  # For standard Python numbers
                return round(value, sig_figs - int(math.floor(math.log10(abs(value)))) - 1)

        # Apply significant figures rounding to all elements in a matrix
        def apply_sf(matrix, sig_figs):
            return matrix.applyfunc(lambda x: round_sf(x, sig_figs))

        augmented_matrix = self.matrixA.row_join(self.matrixB)
        rows, cols = augmented_matrix.shape

        # Forward elimination
        for i in range(rows):
            if not self._isSymbolic(augmented_matrix):
                # Partial pivoting: Find the maximum absolute value in the current column
                max_row = max(range(i, rows), key=lambda r: abs(augmented_matrix[r, i]))
                if max_row != i:
                    augmented_matrix.row_swap(i, max_row)

            # Make the diagonal element 1 by dividing the row
            pivot = augmented_matrix[i, i]
            if pivot == 0:
                raise ValueError("Matrix is singular or nearly singular.")
            augmented_matrix[i, :] = augmented_matrix[i, :] / pivot
            augmented_matrix = apply_sf(augmented_matrix, sf)

            # Make all elements below the pivot in this column zero
            for j in range(i + 1, rows):
                factor = augmented_matrix[j, i]
                augmented_matrix[j, :] -= factor * augmented_matrix[i, :]
                augmented_matrix = apply_sf(augmented_matrix, sf)
            self._solution_line.append(augmented_matrix.copy())

        # Back substitution to solve for variables
        x = sp.zeros(rows, 1)
        for i in range(rows - 1, -1, -1):
            x[i] = augmented_matrix[i, -1] - sum(augmented_matrix[i, j] * x[j] for j in range(i + 1, cols - 1))
            x[i] = round_sf(x[i], sf)

        x = x.applyfunc(sp.simplify)
        self._solution_line.append(x)
        return self._solution_line

    def _isSymbolic(self, augmented_matrix):
        rows, cols = augmented_matrix.shape
        for i in range(rows):
            for j in range(cols):
                if augmented_matrix[i, j].free_symbols:
                    return True
        return False
