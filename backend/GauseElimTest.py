import sympy as sp

def gauss_elimination(matrix, b, isSymbolic):

    # Ensure inputs are SymPy matrices for symbolic and numerical support
    A = sp.Matrix(matrix)
    b = sp.Matrix(b)
    
    # Augment the matrix
    augmented_matrix = A.row_join(b)
    rows, cols = augmented_matrix.shape
    
    # Forward elimination
    for i in range(rows):
        # Apply pivoting only if the matrix is numeric
        if not isSymbolic:
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

    # Back substitution to solve for variables
    x = sp.zeros(rows, 1)
    for i in range(rows - 1, -1, -1):
        x[i] = augmented_matrix[i, -1] - sum(augmented_matrix[i, j] * x[j] for j in range(i + 1, cols - 1))
 
    x = x.applyfunc(sp.simplify)
    return x

# Example: Symbolic
A_symbolic = [[sp.Symbol('a11'), sp.Symbol('a12')], [sp.Symbol('a21'), sp.Symbol('a22')]]
b_symbolic = [sp.Symbol('b1'), sp.Symbol('b2')]

solution_symbolic = gauss_elimination(A_symbolic, b_symbolic, isSymbolic=True)
print("Symbolic Solution:")
sp.pprint(solution_symbolic)

# Example: Numeric
A_numeric = [[2, 1], [1, -1]]
b_numeric = [4, 1]

solution_numeric = gauss_elimination(A_numeric, b_numeric, isSymbolic=False)
print("\nNumeric Solution (With Pivoting):")
print(solution_numeric)

# Mixed symbolic and numeric example
A_mixed = [[2, sp.Symbol('x')], [1, -1]]
b_mixed = [4, sp.Symbol('y')]

solution_mixed = gauss_elimination(A_mixed, b_mixed, isSymbolic=True)
print("Solution for Mixed Numeric and Symbolic Matrix:")
sp.pprint(solution_mixed)

