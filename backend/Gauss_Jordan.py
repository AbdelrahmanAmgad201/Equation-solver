from .parser import Parser
import sympy as sp

class Gauss_Jordan:
    _solution_line = []
    def __init__(self,parser):
        # Create an instance of Parser to handle input
        self._solution_line = []
        self.matrixA = parser.get_matrixA()
        self.matrixB = parser.get_matrixB()


    def solve(self):
        augmented_matrix = sp.Matrix(self.matrixA).row_join(sp.Matrix(self.matrixB).reshape(len(self.matrixB), 1))
        row_len = augmented_matrix.rows  # Number of rows
        col_num = augmented_matrix.cols  # Number of columns

        # Perform Gauss-Jordan Elimination
        for i in range(row_len):
            # Pivot: Find the row with the largest absolute value in the current column
            max_row = max(range(i, row_len), key=lambda r: abs(augmented_matrix[r, i]))
            if not self._isSymbolic(augmented_matrix):
                if max_row != i:
                    augmented_matrix.row_swap(i, max_row)  # Swap rows

            # Normalize the pivot row
            pivot = augmented_matrix[i, i]
            if pivot == 0:
                raise ValueError(f"Matrix is singular or does not have a unique solution.")
            augmented_matrix.row_op(i, lambda x, _: x / pivot)  # Divide the row by the pivot

            # Eliminate all other rows
            for j in range(row_len):
                if i != j:
                    factor = augmented_matrix[j, i]
                    augmented_matrix.row_op(j, lambda x, k: x - factor * augmented_matrix[i, k])

            # Append the current state of the matrix to the solution log
            self._solution_line.append(augmented_matrix.copy())
        self._solution_line.append(augmented_matrix[:,-1])
        return self._solution_line
    def _isSymbolic(self,augmented_matrix):
        rows, cols = augmented_matrix.shape
        for i in range(rows):
            for j in range(cols):
                if augmented_matrix[i, j].free_symbols:
                    return True

        return False



