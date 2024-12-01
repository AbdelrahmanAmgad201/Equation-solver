from PyQt5 import QtWidgets, QtCore


class MatrixDisplayWindow(QtWidgets.QWidget):
    def __init__(self, matrix_3d):
        super().__init__()

        self.setWindowTitle("3D Matrix Display")  # Title for the window
        self.matrix_3d = matrix_3d
        self.current_index = 0  # Start with the first 2D matrix

        self.init_ui()
        self.update_display()

    def init_ui(self):
        """Initialize the user interface."""
        layout = QtWidgets.QVBoxLayout(self)

        # Table widget to display the current 2D matrix
        self.table_widget = QtWidgets.QTableWidget(self)
        self.table_widget.setWordWrap(True)  # Enable word wrapping in cells
        self.table_widget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Interactive)
        self.table_widget.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.table_widget.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)

        # Scroll area for the table to allow scrolling if the matrix is large
        self.scroll_area = QtWidgets.QScrollArea(self)
        self.scroll_area.setWidget(self.table_widget)
        self.scroll_area.setWidgetResizable(True)  # Allow resizing
        layout.addWidget(self.scroll_area)

        # Navigation buttons
        button_layout = QtWidgets.QHBoxLayout()
        self.prev_button = QtWidgets.QPushButton("Prev", self)
        self.next_button = QtWidgets.QPushButton("Next", self)

        # Connect buttons to their respective handlers
        self.prev_button.clicked.connect(self.show_prev_matrix)
        self.next_button.clicked.connect(self.show_next_matrix)

        button_layout.addWidget(self.prev_button)
        button_layout.addWidget(self.next_button)

        # Add navigation buttons to the main layout
        layout.addLayout(button_layout)

        # Disable the "Prev" button initially since we're starting at the first 2D matrix
        self.prev_button.setEnabled(False)

        # Set the window's minimum size based on matrix dimensions
        self.set_minimum_size()

    def set_minimum_size(self):
        """Set the minimum window size based on the matrix dimensions."""
        if not self.matrix_3d:
            return

        # Assume a cell size of 50px width and 30px height (adjust as needed)
        cell_width = 50
        cell_height = 30

        # Get the number of rows and columns of the current 2D matrix
        rows = len(self.matrix_3d[self.current_index])
        cols = len(self.matrix_3d[self.current_index][0]) if rows > 0 else 0

        # Calculate the minimum size for the window
        min_width = cols * cell_width + 100  # Adding some padding for buttons and borders
        min_height = rows * cell_height + 150  # Adding some padding for buttons and title

        # Set the minimum size of the window
        self.setMinimumSize(min_width, min_height)

    def update_display(self):
        """Update the table to show the current 2D matrix."""
        current_matrix = self.matrix_3d[self.current_index]

        # Set the dimensions of the QTableWidget
        rows = len(current_matrix)
        cols = len(current_matrix[0]) if rows > 0 else 0
        self.table_widget.setRowCount(rows)
        self.table_widget.setColumnCount(cols)

        # Populate the QTableWidget with the values of the current 2D matrix
        for i in range(rows):
            for j in range(cols):
                item = QtWidgets.QTableWidgetItem(str(current_matrix[i][j]))
                item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)  # Make item non-editable
                self.table_widget.setItem(i, j, item)

        # Auto resize rows and columns to fit content
        self.table_widget.resizeRowsToContents()
        self.table_widget.resizeColumnsToContents()

        # Update button states
        self.prev_button.setEnabled(self.current_index > 0)
        self.next_button.setEnabled(self.current_index < len(self.matrix_3d) - 1)

        # Update the minimum size after updating the display
        self.set_minimum_size()

    def show_prev_matrix(self):
        """Display the previous 2D matrix in the 3D matrix."""
        if self.current_index > 0:
            self.current_index -= 1
            self.update_display()

    def show_next_matrix(self):
        """Display the next 2D matrix in the 3D matrix."""
        if self.current_index < len(self.matrix_3d) - 1:
            self.current_index += 1
            self.update_display()

