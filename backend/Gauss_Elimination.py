from .parser import Parser
import numpy as np
from sympy import Matrix as SympyMatrix

class Gauss_Elimination:
    def __init__(self):
        # Create an instance of Parser to handle input
        self.parser = Parser()
        self.matrixA = None
        self.matrixB = None

    def initialize_matrices(self):

        # Use the parser to extract matrices
        self.matrixA = self.parser.get_matrixA()
        self.matrixB = self.parser.get_matrixB()

    def solve(self):
        if isinstance(self.matrixA, np.ndarray):
            return self._solve_numerical()
        elif isinstance(self.matrixA, SympyMatrix):
            return self._solve_symbolic()

    def __solve_Numerical(self):
        """
            Solves the system numerically using NumPy operations.
        """
        pass
    def __solve_Symbolic(self):
        """
            Solves the system symbolically using SymPy operations.
        """
        pass