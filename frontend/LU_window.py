from PyQt5 import QtWidgets, QtCore


class DualMatrixDisplayWindow(QtWidgets.QWidget):
    def __init__(self, matrix_3d_1, matrix_3d_2):
        super().__init__()

        self.setWindowTitle("LU Matrix Display")  # Title for the window
        self.matrix_3d_1 = matrix_3d_1
        self.matrix_3d_2 = matrix_3d_2
        self.current_index_1 = 0  # Start with the first 2D matrix of matrix_3d_1
        self.current_index_2 = 0  # Start with the first 2D matrix of matrix_3d_2

        self.init_ui()
        self.update_display()

    def init_ui(self):
        """Initialize the user interface."""
        layout = QtWidgets.QHBoxLayout(self)

        # Table widgets to display the current 2D matrices
        self.table_widget_1 = QtWidgets.QTableWidget(self)
        self.table_widget_2 = QtWidgets.QTableWidget(self)

        # Enable word wrapping
        self.table_widget_1.setWordWrap(True)
        self.table_widget_2.setWordWrap(True)

        # Configure horizontal and vertical headers to stretch with content
        self.table_widget_1.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.table_widget_1.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.table_widget_2.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.table_widget_2.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        # Scroll area for both tables to allow scrolling if the matrices are large
        self.scroll_area_1 = QtWidgets.QScrollArea(self)
        self.scroll_area_2 = QtWidgets.QScrollArea(self)

        self.scroll_area_1.setWidget(self.table_widget_1)
        self.scroll_area_2.setWidget(self.table_widget_2)

        self.scroll_area_1.setWidgetResizable(True)  # Allow resizing
        self.scroll_area_2.setWidgetResizable(True)  # Allow resizing

        layout.addWidget(self.scroll_area_1)
        layout.addWidget(self.scroll_area_2)

        # Navigation buttons for both matrices
        button_layout = QtWidgets.QVBoxLayout()
        self.prev_button_1 = QtWidgets.QPushButton("Prev (Lower)", self)
        self.next_button_1 = QtWidgets.QPushButton("Next (Lower)", self)
        self.prev_button_2 = QtWidgets.QPushButton("Prev (Upper)", self)
        self.next_button_2 = QtWidgets.QPushButton("Next (Upper)", self)

        # Connect buttons to their respective handlers
        self.prev_button_1.clicked.connect(self.show_prev_matrix_1)
        self.next_button_1.clicked.connect(self.show_next_matrix_1)
        self.prev_button_2.clicked.connect(self.show_prev_matrix_2)
        self.next_button_2.clicked.connect(self.show_next_matrix_2)

        # Add navigation buttons for both matrices to the layout
        button_layout.addWidget(self.prev_button_1)
        button_layout.addWidget(self.next_button_1)
        button_layout.addWidget(self.prev_button_2)
        button_layout.addWidget(self.next_button_2)

        layout.addLayout(button_layout)

        # Disable the "Prev" button initially since we're starting at the first 2D matrix
        self.prev_button_1.setEnabled(False)
        self.prev_button_2.setEnabled(False)

        # Set the window's minimum size based on matrix dimensions
        self.set_minimum_size()

    def set_minimum_size(self):
        """Set the minimum window size based on the matrix dimensions."""
        if not self.matrix_3d_1 or not self.matrix_3d_2:
            return

        # Assume a cell size of 50px width and 30px height (adjust as needed)
        cell_width = 50
        cell_height = 30

        # Get the number of rows and columns of the current 2D matrix for both matrices
        rows_1 = len(self.matrix_3d_1[self.current_index_1])
        cols_1 = len(self.matrix_3d_1[self.current_index_1][0]) if rows_1 > 0 else 0

        rows_2 = len(self.matrix_3d_2[self.current_index_2])
        cols_2 = len(self.matrix_3d_2[self.current_index_2][0]) if rows_2 > 0 else 0

        # Calculate the minimum size for the window
        min_width = max(cols_1, cols_2) * cell_width + 150  # Adding some padding for buttons and borders
        min_height = max(rows_1, rows_2) * cell_height + 150  # Adding some padding for buttons and title

        # Set the minimum size of the window
        self.setMinimumSize(min_width, min_height)

    def update_display(self):
        """Update the table to show the current 2D matrix for both matrices."""
        # For matrix 1
        current_matrix_1 = self.matrix_3d_1[self.current_index_1]
        rows_1 = len(current_matrix_1)
        cols_1 = len(current_matrix_1[0]) if rows_1 > 0 else 0
        self.table_widget_1.setRowCount(rows_1)
        self.table_widget_1.setColumnCount(cols_1)

        for i in range(rows_1):
            for j in range(cols_1):
                item = QtWidgets.QTableWidgetItem(str(current_matrix_1[i][j]))
                item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)  # Make item non-editable
                self.table_widget_1.setItem(i, j, item)

        self.table_widget_1.resizeRowsToContents()
        self.table_widget_1.resizeColumnsToContents()

        # For matrix 2
        current_matrix_2 = self.matrix_3d_2[self.current_index_2]
        rows_2 = len(current_matrix_2)
        cols_2 = len(current_matrix_2[0]) if rows_2 > 0 else 0
        self.table_widget_2.setRowCount(rows_2)
        self.table_widget_2.setColumnCount(cols_2)

        for i in range(rows_2):
            for j in range(cols_2):
                item = QtWidgets.QTableWidgetItem(str(current_matrix_2[i][j]))
                item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)  # Make item non-editable
                self.table_widget_2.setItem(i, j, item)

        self.table_widget_2.resizeRowsToContents()
        self.table_widget_2.resizeColumnsToContents()

        # Update button states
        self.prev_button_1.setEnabled(self.current_index_1 > 0)
        self.next_button_1.setEnabled(self.current_index_1 < len(self.matrix_3d_1) - 1)

        self.prev_button_2.setEnabled(self.current_index_2 > 0)
        self.next_button_2.setEnabled(self.current_index_2 < len(self.matrix_3d_2) - 1)

        # Update the minimum size after updating the display
        self.set_minimum_size()

    def show_prev_matrix_1(self):
        """Display the previous 2D matrix in matrix_3d_1."""
        if self.current_index_1 > 0:
            self.current_index_1 -= 1
            self.update_display()

    def show_next_matrix_1(self):
        """Display the next 2D matrix in matrix_3d_1."""
        if self.current_index_1 < len(self.matrix_3d_1) - 1:
            self.current_index_1 += 1
            self.update_display()

    def show_prev_matrix_2(self):
        """Display the previous 2D matrix in matrix_3d_2."""
        if self.current_index_2 > 0:
            self.current_index_2 -= 1
            self.update_display()

    def show_next_matrix_2(self):
        """Display the next 2D matrix in matrix_3d_2."""
        if self.current_index_2 < len(self.matrix_3d_2) - 1:
            self.current_index_2 += 1
            self.update_display()

