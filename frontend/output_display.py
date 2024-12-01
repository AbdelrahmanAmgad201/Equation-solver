from PyQt5 import QtWidgets, QtGui, QtCore
import sys
import numpy as np  # For creating and handling 3D arrays


class ArrayDisplayPage(QtWidgets.QWidget):
    def __init__(self, array_3d, parent=None):
        super().__init__(parent)
        self.array_3d = array_3d  # Store the 3D array
        self.current_index = 0   # Track the current 2D slice

        # Initialize UI
        self.init_ui()

    def init_ui(self):
        # Main layout
        self.layout = QtWidgets.QVBoxLayout(self)

        # Label to display the current 2D matrix
        self.matrix_label = QtWidgets.QLabel(self)
        self.matrix_label.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.matrix_label)

        # Navigation buttons
        button_layout = QtWidgets.QHBoxLayout()

        self.prev_button = QtWidgets.QPushButton("Prev", self)
        self.next_button = QtWidgets.QPushButton("Next", self)

        button_layout.addWidget(self.prev_button)
        button_layout.addWidget(self.next_button)

        self.layout.addLayout(button_layout)

        # Connect button signals
        self.prev_button.clicked.connect(self.show_prev_matrix)
        self.next_button.clicked.connect(self.show_next_matrix)

        # Display the first 2D matrix
        self.update_display()

    def update_display(self):
        """Update the display with the current 2D matrix."""
        if 0 <= self.current_index < len(self.array_3d):
            matrix = self.array_3d[self.current_index]
            matrix_text = self.format_matrix(matrix)
            self.matrix_label.setText(f"Matrix {self.current_index + 1}:\n{matrix_text}")

            # Enable or disable buttons based on the index
            self.prev_button.setEnabled(self.current_index > 0)
            self.next_button.setEnabled(self.current_index < len(self.array_3d) - 1)

    def format_matrix(self, matrix):
        """Format the 2D matrix as a string for display."""
        return "\n".join(["\t".join(map(str, row)) for row in matrix])

    def show_prev_matrix(self):
        """Show the previous 2D matrix."""
        if self.current_index > 0:
            self.current_index -= 1
            self.update_display()

    def show_next_matrix(self):
        """Show the next 2D matrix."""
        if self.current_index < len(self.array_3d) - 1:
            self.current_index += 1
            self.update_display()


# Example usage
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    # Example 3D array
    array_3d = np.array([
        [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
        [[9, 8, 7], [6, 5, 4], [3, 2, 1]],
        [[2, 4, 6], [8, 10, 12], [14, 16, 18]]
    ])

    # Create and show the display page
    window = ArrayDisplayPage(array_3d)
    window.setWindowTitle("3D Array Viewer")
    window.resize(400, 300)
    window.show()

    sys.exit(app.exec_())
