import sympy as sp

# Input matrices
matrixA = [
    [2, 1, -1],
    [-3, -1, 2],
    [-2, 1, 2]
]
matrixB = [8, -11, -3]

# Create augmented matrix
augmented_matrix = sp.Matrix(matrixA).row_join(sp.Matrix(matrixB).reshape(len(matrixB), 1))
print("Augmented Matrix:")
sp.pprint(augmented_matrix)

row_len = augmented_matrix.rows  # Number of rows
col_num = augmented_matrix.cols  # Number of columns
_solution_line = []

# Perform Gauss-Jordan Elimination
for i in range(row_len):
    # Pivot: Find the row with the largest absolute value in the current column
    max_row = max(range(i, row_len), key=lambda r: abs(augmented_matrix[r, i]))
    if max_row != i:
        augmented_matrix.row_swap(i, max_row)  #

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
    _solution_line.append(augmented_matrix.copy())

# Display each step in the solution process
print("\nSolution Steps:")
for i, step in enumerate(_solution_line):
    print(f"Step {i + 1}:")
    sp.pprint(step)

# Extract the solution
solution = [augmented_matrix[i, -1] for i in range(row_len)]
print("\nSolution:")
sp.pprint(solution)

