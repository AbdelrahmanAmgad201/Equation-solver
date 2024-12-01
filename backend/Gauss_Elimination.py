from .parser import Parser
import numpy as np
import sympy as sp
import math

class Gauss_Elimination:
    _solution_line = []
    def __init__(self,parser):
        self._solution_line = []
        self.matrixA = parser.get_matrixA()
        self.matrixB = parser.get_matrixB()


    def solve(self):

        augmented_matrix = self.matrixA.row_join(self.matrixB)
        rows, cols = augmented_matrix.shape

        # Forward elimination
        for i in range(rows):

            if not self._isSymbolic(augmented_matrix):

                # Find the maximum absolute value in the current column for partial pivoting
                max_row = max(range(i, rows), key=lambda r: abs(augmented_matrix[r, i]))
                # Swap rows if necessary
                if max_row != i:
                    augmented_matrix.row_swap(i, max_row)

            # Make the diagonal element 1 by dividing the row
            pivot = augmented_matrix[i, i]
            if pivot == 0:
                raise ValueError("Matrix is singular or nearly singular.")
            augmented_matrix[i, :] = augmented_matrix[i, :] / pivot

            # Make all elements below the pivot in this column zero
            for j in range(i + 1, rows):
                factor = augmented_matrix[j, i]
                augmented_matrix[j, :] -= factor * augmented_matrix[i, :]
            self._solution_line.append(augmented_matrix.copy())


        # Back substitution to solve for variables
        x = sp.zeros(rows, 1)
        for i in range(rows - 1, -1, -1):
            x[i] = augmented_matrix[i, -1] - sum(augmented_matrix[i, j] * x[j] for j in range(i + 1, cols - 1))

        x = x.applyfunc(sp.simplify)

        self._solution_line.append(x)
        return self._solution_line
    def _isSymbolic(self,augmented_matrix):
        rows, cols = augmented_matrix.shape
        for i in range(rows):
            for j in range(cols):
                if augmented_matrix[i, j].free_symbols:
                    return True

        return False

