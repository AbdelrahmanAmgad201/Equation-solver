from .parser import Parser
import sympy as sp
import math


class LU_Decomposition:
    def __init__(self, parser):
        self.matrixA = parser.get_matrixA()
        self.matrixB = parser.get_matrixB()

    def _round_sf(self, value, sig_figs):
        if isinstance(value, sp.Basic):  # SymPy type
            return value.evalf(sig_figs) if value.is_number else value
        elif value == 0:
            return 0
        else:  # Standard numeric type
            return round(value, sig_figs - int(math.floor(math.log10(abs(value)))) - 1)

    def _apply_sf(self, matrix, sig_figs):
        return matrix.applyfunc(lambda x: self._round_sf(x, sig_figs))

    def solve_LU_Doolittle(self, sf):
        """Perform LU decomposition using Doolittle's method with partial pivoting and significant figures."""
        sf = int(sf)
        n = self.matrixA.shape[0]
        L = sp.Matrix.zeros(n)
        U = self.matrixA.copy()
        P = sp.eye(n)  # Permutation matrix

        for i in range(n):
            # Partial pivoting: Find the max element in the current column
            if not self._isSymbolic(self.matrixA) and self._isSymbolic(self.matrixB):
                pivot_row = max(range(i, n), key=lambda r: abs(U[r, i]))
                if i != pivot_row:
                # Swap rows in U
                    U.row_swap(i, pivot_row)
                # Swap rows in P
                    P.row_swap(i, pivot_row)
                # Swap rows in L (only for the columns computed so far)
                    if i > 0:
                        L.row_swap(i, pivot_row)

            # Upper Triangular Matrix U
            for k in range(i, n):
                U[i, k] = U[i, k] - sum(L[i, j] * U[j, k] for j in range(i))
                U[i, k] = self._round_sf(U[i, k], sf)

            # Lower Triangular Matrix L
            for k in range(i + 1, n):
                L[k, i] = (U[k, i] - sum(L[k, j] * U[j, i] for j in range(i))) / U[i, i]
                L[k, i] = self._round_sf(L[k, i], sf)

        # Set diagonal of L to 1
        for i in range(n):
            L[i, i] = 1

        # Adjust B according to the permutation matrix P
        B_permuted = P * self.matrixB

        # Solve LY = B and UX = Y
        Y = self._forward_substitution(L, B_permuted, sf)
        X = self._backward_substitution(U, Y, sf)

        return [P, L, U, X]

    def solve_LU_Crout(self, sf):
        sf = int(sf)
        n = self.matrixA.shape[0]
        L = sp.Matrix.zeros(n)
        U = sp.eye(n)

        for j in range(n):
            # Check if pivot is zero
            if self.matrixA[j, j] == 0:
                raise ZeroDivisionError(f"Pivot element is zero at row {j}. Cannot perform LU decomposition.")

            # Compute L's column
            for i in range(j, n):
                L[i, j] = self.matrixA[i, j] - sum(L[i, k] * U[k, j] for k in range(j))
                L[i, j] = self._round_sf(L[i, j], sf)

            # Compute U's row
            for i in range(j + 1, n):
                U[j, i] = (self.matrixA[j, i] - sum(L[j, k] * U[k, i] for k in range(j))) / L[j, j]
                U[j, i] = self._round_sf(U[j, i], sf)

        Y = self._forward_substitution(L, self.matrixB, sf)
        X = self._backward_substitution(U, Y, sf)

        return [L, U, X]

    def _forward_substitution(self, L, b, sf):
        n = len(b)
        y = sp.Matrix.zeros(n, 1)

        for i in range(n):
            y[i] = (b[i] - sum(L[i, j] * y[j] for j in range(i))) / L[i, i]
            y[i] = self._round_sf(y[i], sf)

        return y

    def _backward_substitution(self, U, y, sf):
        n = len(y)
        x = sp.Matrix.zeros(n, 1)

        for i in range(n - 1, -1, -1):
            x[i] = (y[i] - sum(U[i, j] * x[j] for j in range(i + 1, n))) / U[i, i]
            x[i] = self._round_sf(x[i], sf)

        return x
    def _isSymbolic(self, augmented_matrix):
        rows, cols = augmented_matrix.shape
        for i in range(rows):
            for j in range(cols):
                if augmented_matrix[i, j].free_symbols:
                    return True
        return False
