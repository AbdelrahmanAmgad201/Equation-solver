import sympy as sp

class Parser:
    def __init__(self, augmented_matrix, scaled=False):
        # AX = B
        self.augmented_matrix =sp.Matrix(augmented_matrix)
        if scaled and not self._isSymbolic(self.augmented_matrix):
            self.augmented_matrix = self.scale_matrix(self.augmented_matrix)
            return

    def get_matrixA(self):
        # Get matrix A (all rows, except the last column)
        matrixA = [row[:-1] for row in self.augmented_matrix.tolist()]  # Convert to list and slice
        return sp.Matrix(matrixA)

    def get_matrixB(self):
        # Get matrix B (the last column of the augmented matrix)
        matrixB = [row[-1] for row in self.augmented_matrix.tolist()]  # Convert to list and slice
        return sp.Matrix(matrixB)

    def scale_matrix(self, augmented_matrix):
        # Convert the augmented matrix to a SymPy matrix
        rows, cols = augmented_matrix.shape
        for i in range(rows):
            row = augmented_matrix.row(i)  # Get the i-th row
            max_value = max(abs(val) for val in row)  # Get max absolute value in row
            if max_value != 0:
                # Scale each element in the row manually and assign it back to the matrix
                for j in range(cols):
                    augmented_matrix[i, j] = augmented_matrix[i, j] / max_value
        return augmented_matrix
    def _isSymbolic(self, augmented_matrix):
        rows, cols = augmented_matrix.shape
        for i in range(rows):
            for j in range(cols):
                if augmented_matrix[i, j].free_symbols:
                    return True
        return False



