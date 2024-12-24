from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer
from .main_page import Ui_Form
from .matrix_page import SecondPage
from .display_page import MatrixDisplayWindow
from .LU_window import DualMatrixDisplayWindow
from .constants import WIDTH, HEIGHT
from .observers import Observer
from .getRoot import MyWindow as Phase2
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

        self.phase1_page = QtWidgets.QWidget(self)
        self.ui_form = Ui_Form()
        self.ui_form.setupUi(self.phase1_page)

        self.matrix_page = SecondPage()

        self.phase2_page = Phase2()

        # New page (page 3)
        self.start_page = QtWidgets.QWidget(self)
        self.start_page_layout = QtWidgets.QVBoxLayout(self.start_page)
        self.phase1_button = QtWidgets.QPushButton("PHASE 1", self.start_page)
        self.start_page_layout.addWidget(self.phase1_button)

        self.phase2_button = QtWidgets.QPushButton("PHASE 2", self.start_page)
        self.start_page_layout.addWidget(self.phase2_button)

        self.start_page.setLayout(self.start_page_layout)

        self.stacked_widget.setGeometry(0, 0, WIDTH, HEIGHT)

        self.stacked_widget.addWidget(self.start_page)
        self.stacked_widget.addWidget(self.phase1_page)
        self.stacked_widget.addWidget(self.matrix_page)
        self.stacked_widget.addWidget(self.phase2_page)


        self.stacked_widget.setCurrentIndex(0)
        self.ui_form.pushButton.clicked.connect(self.go_to_matrix_input_page)
        self.ui_form.backButton.clicked.connect(self.go_to_start)

        self.phase2_page.back_button.clicked.connect(self.go_to_start)


        
        # Connect the new button to the function to switch pages
        self.phase1_button.clicked.connect(self.go_to_phase1)
        self.phase2_button.clicked.connect(self.go_to_phase2)


        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.stacked_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.setGeometry(100, 100, WIDTH, HEIGHT)
        self.show()

    def go_to_start(self):
        self.stacked_widget.setCurrentIndex(0)


    def go_to_matrix_input_page(self):
        matrix_size = self.ui_form.lineEdit.text()
        digits = self.ui_form.lineEdit_significant_digits.text()

        if (not(digits.isdigit()) or digits == "0") and digits != "":
            QtWidgets.QMessageBox.warning(self, "Invalid Input", "Please enter significant digits.")
            return

        if matrix_size.isdigit() and int(matrix_size) > 0:
            matrix_size = int(matrix_size)
            details = Observer.matrix_details

            # Check if the method is Jacobi or Gauss Seidel
            if details.get('method') in ["Jacobi", "Gauss Seidel"]:
                # Check if initial_vector is empty or contains an empty string
                if not details.get('initial_vector') or '' in details.get('initial_vector'):
                    QtWidgets.QMessageBox.warning(self, "Invalid Input", "Ensure the initial vector is provided!")
                    return
                else:
                    self.matrix_page.display_matrix_entries(matrix_size, matrix_size)
                    self.stacked_widget.setCurrentIndex(2)
            else:
                self.matrix_page.display_matrix_entries(matrix_size, matrix_size)
                self.stacked_widget.setCurrentIndex(2)
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

    def display_error(self, error):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Warning)
        msg.setWindowTitle("Input Error")
        msg.setText(error)
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg.exec_()

    def go_to_phase1(self):
        self.stacked_widget.setCurrentIndex(1)

    def go_to_phase2(self):
        self.stacked_widget.setCurrentIndex(3)

