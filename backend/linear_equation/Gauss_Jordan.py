from .parser import Parser
import sympy as sp
import math

class Gauss_Jordan:
    _solution_line = []

    def __init__(self, parser):
        self._solution_line = []
        self.matrixA = parser.get_matrixA()
        self.matrixB = parser.get_matrixB()

    def solve(self, sf):
        sf = int(sf)

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

        # Augmented matrix: [A | B]
        augmented_matrix = sp.Matrix(self.matrixA).row_join(
            sp.Matrix(self.matrixB).reshape(len(self.matrixB), 1)
        )
        row_len = augmented_matrix.rows  # Number of rows
        col_num = augmented_matrix.cols  # Number of columns

        # Perform Gauss-Jordan Elimination
        for i in range(row_len):
            # Pivot: Find the row with the largest absolute value in the current column
            max_row = max(range(i, row_len), key=lambda r: abs(augmented_matrix[r, i].evalf()))

            if not self._isSymbolic(augmented_matrix):
                if max_row != i:
                    augmented_matrix.row_swap(i, max_row)  # Swap rows

            # Normalize the pivot row
            pivot = augmented_matrix[i, i]
            if pivot == 0:
                raise ValueError("Matrix is singular or does not have a unique solution.")
            augmented_matrix.row_op(i, lambda x, _: round_sf(x / pivot, sf))  # Divide the row by the pivot
            augmented_matrix = apply_sf(augmented_matrix, sf)

            # Eliminate all other rows
            for j in range(row_len):
                if i != j:
                    factor = augmented_matrix[j, i]
                    augmented_matrix.row_op(
                        j, lambda x, k: round_sf(x - factor * augmented_matrix[i, k], sf)
                    )
                    augmented_matrix = apply_sf(augmented_matrix, sf)

            # Append the current state of the matrix to the solution log
            self._solution_line.append(augmented_matrix.copy())

        # Append the final solution (last column of the augmented matrix)
        self._solution_line.append(apply_sf(augmented_matrix[:, -1], sf))
        return self._solution_line

    def _isSymbolic(self, augmented_matrix):
        rows, cols = augmented_matrix.shape
        for i in range(rows):
            for j in range(cols):
                if augmented_matrix[i, j].free_symbols:
                    return True
        return False
