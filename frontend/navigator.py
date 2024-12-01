from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer
from .main_page import Ui_Form
from .matrix_page import SecondPage
from .display_page import MatrixDisplayWindow
from .LU_window import DualMatrixDisplayWindow
from .constants import WIDTH, HEIGHT
from .observers import Observer
import sys

class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_matrix_observer)
        self.timer.start(500)

    def init_ui(self):
        self.setWindowTitle("Main Window with StackedWidget")

        self.stacked_widget = QtWidgets.QStackedWidget(self)

        self.page_1 = QtWidgets.QWidget(self)
        self.ui_form = Ui_Form()
        self.ui_form.setupUi(self.page_1)

        self.page_2 = SecondPage()

        self.stacked_widget.setGeometry(0, 0, WIDTH, HEIGHT)

        self.stacked_widget.addWidget(self.page_1)
        self.stacked_widget.addWidget(self.page_2)

        self.stacked_widget.setCurrentIndex(0)
        self.ui_form.pushButton.clicked.connect(self.go_to_matrix_input_page)

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.stacked_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.setGeometry(100, 100, WIDTH, HEIGHT)
        self.setFixedSize(WIDTH, HEIGHT)
        self.show()

    def go_to_matrix_input_page(self):
        matrix_size = self.ui_form.lineEdit.text()
        digits = self.ui_form.lineEdit_significant_digits.text()

        if not(digits.isdigit() and int(digits) > 0):
            QtWidgets.QMessageBox.warning(self, "Invalid Input", "Please enter significant digits.")
            return

        if matrix_size.isdigit() and int(matrix_size) > 0:
            matrix_size = int(matrix_size)
            details = Observer.matrix_details

            # Check if the method is Jacobi or Gauss Seidel
            if details.get('method') in ["Jacobi", "Gauss Seidel"]:
                # Check if initial_vector is empty or contains an empty string
                if not details.get('iterations') and not details.get('absolute_relative_error') and (not details.get('initial_vector') or details.get('initial_vector') == ['']):
                    QtWidgets.QMessageBox.warning(self, "Invalid Input", "Please enter absolute relative error or iterations, and ensure the initial vector is provided.")
                    return  # Don't proceed to the next page
                elif details.get('initial_vector') == ['']:  # Check if initial_vector is empty ([''])
                    QtWidgets.QMessageBox.warning(self, "Invalid Input", "Initial vector is required for the Jacobi method.")
                    return  # Don't proceed to the next page
                else:
                    self.page_2.display_matrix_entries(matrix_size, matrix_size)
                    self.stacked_widget.setCurrentIndex(1)
            else:
                self.page_2.display_matrix_entries(matrix_size, matrix_size)
                self.stacked_widget.setCurrentIndex(1)
        else:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.setWindowTitle("Input Error")
            msg.setText("Matrix Size should be a valid number!")
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msg.exec_()



    def check_matrix_observer(self):
        if Observer.matrix_observer is not None:
            self.go_to_matrix_display()
            Observer.matrix_observer = None

    def display_matrix(self, matrix_data):
        self.matrix_window = MatrixDisplayWindow(matrix_data)
        self.matrix_window.show()

    def go_to_matrix_display(self, matrix=None):
        if matrix is None:

            return
        self.display_matrix(matrix)

    def display_LU_matrix(self, matrix1, matrix2):
        if matrix1 is None or matrix2 is None:
            return
        self.matrix_window = DualMatrixDisplayWindow(matrix1, matrix2)
        self.matrix_window.show()




