from .parser import Parser
import sympy as sp
import math


class LU_Decomposition:
    def __init__(self, parser):
        self.matrixA = parser.get_matrixA()
        self.matrixB = parser.get_matrixB()

    def _round_sf(self, value, sig_figs):
        if value == 0:
            return 0
        elif isinstance(value, sp.Basic):  # SymPy type
            return value.evalf(sig_figs)
        else:  # Standard numeric type
            return round(value, sig_figs - int(math.floor(math.log10(abs(value)))) - 1)

    def _apply_sf(self, matrix, sig_figs):
        return matrix.applyfunc(lambda x: self._round_sf(x, sig_figs))

    def solve_LU_Doolittle(self, sf):
        sf = int(sf)
        n = self.matrixA.shape[0]
        L = sp.Matrix.zeros(n)
        U = sp.Matrix.zeros(n)

        for i in range(n):
            # Upper Triangular Matrix U
            for k in range(i, n):
                U[i, k] = self.matrixA[i, k] - sum(L[i, j] * U[j, k] for j in range(i))
                U[i, k] = self._round_sf(U[i, k], sf)

            # Lower Triangular Matrix L
            for k in range(i, n):
                if i == k:
                    L[i, i] = 1  # Diagonal as 1
                else:
                    L[k, i] = (self.matrixA[k, i] - sum(L[k, j] * U[j, i] for j in range(i))) / U[i, i]
                    L[k, i] = self._round_sf(L[k, i], sf)

        Y = self._forward_substitution(L, self.matrixB, sf)
        X = self._backward_substitution(U, Y, sf)

        return [L, U, X]

    def solve_LU_Crout(self, sf):
        sf = int(sf)
        n = self.matrixA.shape[0]
        L = sp.Matrix.zeros(n)
        U = sp.eye(n)

        for j in range(n):
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

    def solve_LU_Cholesky(self, sf):
        sf = int(sf)
        if not self._symmetric_positive_definite():
            raise Exception("The matrix is not positive definite")

        L = self._cholesky(sf)
        Y = self._forward_substitution(L, self.matrixB, sf)
        X = self._backward_substitution(L.T, Y, sf)

        return [L, L.T, X]

    def _symmetric_positive_definite(self):
        eigenvalues = self.matrixA.eigenvals()

        # Verify that all eigenvalues are positive
        for eigenvalue in eigenvalues:
            if not (eigenvalue > 0):
                return False

        return True

    def _cholesky(self, sf):
        sf = int(sf)
        n = self.matrixA.shape[0]
        L = sp.Matrix.zeros(n)

        for i in range(n):
            for j in range(i + 1):
                if i == j:
                    L[i, j] = sp.sqrt(self.matrixA[i, j] - sum(L[i, k] ** 2 for k in range(j)))
                else:
                    L[i, j] = (self.matrixA[i, j] - sum(L[i, k] * L[j, k] for k in range(j))) / L[j, j]
                L[i, j] = self._round_sf(L[i, j], sf)

        return L

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
