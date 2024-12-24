from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QComboBox,
    QVBoxLayout, QHBoxLayout, QWidget, QLineEdit, QPushButton
)
import sys
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import math
import time
from .result_window import ResultWindow
from .solver import Solver
from .steps import TableWindow

class MyWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Get Root")
        self.initUI()
        self.solver = Solver()
        self.error_msg = ""

    def initUI(self):
        self.setGeometry(100, 100, 1000, 800)  # Window size and position



        self.setStyleSheet("""
            QLineEdit {
                border-radius: 5px;
                padding: 5px;
                font-size: 20px;
            }

            * {
                font-size: 20px;
            }
        """)
        
        self.error_label = QLabel("")
        self.error_label.setAlignment(Qt.AlignCenter)
        self.error_label.setStyleSheet("background-color: red; color: white; font-weight: bold;"
                                       "padding: 10px;"
                                       "font-size: 24px;")
        self.error_label.hide()

        # Title label in the middle
        title_label = QLabel("Calculate root of equation", self)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 24px")

        # Label and dropdown list
        method_label = QLabel("Method:")
        self.dropdown = QComboBox()
        self.dropdown.addItems(["Bisection",
                           "False-Position",
                           "Fixed point",
                           "Original Newton-Raphson",
                           "Modified Newton-Raphson",
                           "Secant"])  # Add dropdown items
        
        # Equation and G(x) inputs
        self.equation_label = QLabel("Equation:")
        self.equation_input = QLineEdit()
        self.gx_label = QLabel("G(x):")
        self.gx_input = QLineEdit()

         # Initially hide G(x) input
        self.gx_label.hide()
        self.gx_input.hide()

        self.dropdown.currentIndexChanged.connect(self.handle_dropdown_change)

        self.plot_button = QPushButton("Plot Graph")
        self.plot_button.clicked.connect(self.plot_graph)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setMinimumSize(100, 100)

        sig_fig_label = QLabel("Number of Significant Figures:")
        self.sig_fig_input = QLineEdit()

        max_iter_label = QLabel("Maximum Iterations:")
        self.max_iter_input = QLineEdit()

        tolerance_label = QLabel("Tolerance:")
        self.tolerance_input = QLineEdit()

        self.low_label = QLabel("Low:")
        self.low_input = QLineEdit()

        self.high_label = QLabel("High:")
        self.high_input = QLineEdit()

        self.intial_guess_label = QLabel("Intial Guess:")
        self.intial_guess_input = QLineEdit()

        self.intial_guess_label.hide()
        self.intial_guess_input.hide()

        intial_guess_layout = QHBoxLayout()
        intial_guess_layout.addWidget(self.intial_guess_label)
        intial_guess_layout.addWidget(self.intial_guess_input)

        self.intial_secant_points = QLabel("Intial Points:")
        self.secant_p1 = QLabel("P1:")
        self.secant_p1_input = QLineEdit()
        self.secant_p2 = QLabel("P2:")
        self.secant_p2_input = QLineEdit()

        self.intial_secant_points.hide()
        self.secant_p1.hide()
        self.secant_p2.hide()
        self.secant_p1_input.hide()
        self.secant_p2_input.hide()  

        secant_intials_layout = QHBoxLayout()
        secant_intials_layout.addWidget(self.intial_secant_points)
        secant_intials_layout.addWidget(self.secant_p1)      
        secant_intials_layout.addWidget(self.secant_p1_input)
        secant_intials_layout.addWidget(self.secant_p2)
        secant_intials_layout.addWidget(self.secant_p2_input)

        get_root_button = QPushButton("Get Root")
        get_root_button.clicked.connect(self.get_root)
        get_root_button.setStyleSheet("font-size: 24px;"
                                      "padding: 10px 30px;"
                                      "font-weight: 500;")
        


        # Centering the "Get Root" button in a QHBoxLayout
        root_button_layout = QHBoxLayout()
        root_button_layout.addStretch(1)  # Adds stretchable space before the button
        root_button_layout.addWidget(get_root_button)
        root_button_layout.addStretch(1)  # Adds stretchable space after the button


        self.back_button = QPushButton("BACK")
        self.back_button.setStyleSheet("font-size: 24px;"
                                      "padding: 10px 30px;"
                                      "font-weight: 500;")
        
                # Centering the "Get Root" button in a QHBoxLayout
        back_button_layout = QHBoxLayout()
        back_button_layout.addStretch(1)  # Adds stretchable space before the button
        back_button_layout.addWidget(self.back_button)
        back_button_layout.addStretch(1)  # Adds stretchable space after the button
        # Layouts
        sig_fig_layout = QHBoxLayout()
        sig_fig_layout.addWidget(sig_fig_label)
        sig_fig_layout.addWidget(self.sig_fig_input)

        max_iter_layout = QHBoxLayout()
        max_iter_layout.addWidget(max_iter_label)
        max_iter_layout.addWidget(self.max_iter_input)

        tolerance_layout = QHBoxLayout()
        tolerance_layout.addWidget(tolerance_label)
        tolerance_layout.addWidget(self.tolerance_input)

        method_layout = QHBoxLayout()
        method_layout.addWidget(method_label)
        method_layout.addWidget(self.dropdown)

        equation_layout = QHBoxLayout()
        equation_layout.addWidget(self.equation_label)
        equation_layout.addWidget(self.equation_input)

        gx_layout = QHBoxLayout()
        gx_layout.addWidget(self.gx_label)
        gx_layout.addWidget(self.gx_input)

        low_high_layout = QHBoxLayout()
        low_high_layout.addWidget(self.low_label)
        low_high_layout.addWidget(self.low_input)
        low_high_layout.addWidget(self.high_label)
        low_high_layout.addWidget(self.high_input)

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(title_label)
        main_layout.addWidget(self.error_label)
        main_layout.addLayout(method_layout)
        main_layout.addLayout(equation_layout)
        main_layout.addLayout(gx_layout)
        main_layout.addWidget(self.plot_button)
        main_layout.addWidget(self.canvas)
        main_layout.addLayout(sig_fig_layout)
        main_layout.addLayout(max_iter_layout)
        main_layout.addLayout(tolerance_layout)
        main_layout.addLayout(low_high_layout)
        main_layout.addLayout(intial_guess_layout)
        main_layout.addLayout(secant_intials_layout)
        main_layout.addLayout(root_button_layout)
        main_layout.addLayout(back_button_layout)

    
    def handle_dropdown_change(self, index):
        self.hide_all_extra_input()
        idx = self.dropdown.currentIndex()
        if idx == 0 or idx == 1:
            self.show_bisection_input()
        if idx == 2:
            self.show_gx_input()
        
        if idx in [2,3,4]:
            self.show_intial_guess()

        if idx == 5:
            self.show_intial_secant_input()

    def show_gx_input(self):
        self.gx_label.show()
        self.gx_input.show()

    def show_bisection_input(self):
        self.low_label.show()
        self.low_input.show()
        self.high_label.show()
        self.high_input.show()

    def show_intial_guess(self):
        self.intial_guess_label.show()
        self.intial_guess_input.show()

    def show_intial_secant_input(self):
        self.intial_secant_points.show()
        self.secant_p1.show()
        self.secant_p2.show()
        self.secant_p1_input.show()
        self.secant_p2_input.show()

    def hide_all_extra_input(self):
        self.gx_label.hide()
        self.gx_input.hide()
        self.low_label.hide()
        self.low_input.hide()
        self.high_label.hide()
        self.high_input.hide()
        self.intial_guess_label.hide()
        self.intial_guess_input.hide()
        self.intial_secant_points.hide()
        self.secant_p1.hide()
        self.secant_p2.hide()
        self.secant_p1_input.hide()
        self.secant_p2_input.hide()
        

    def plot_graph(self):
        try:
            equation = self.equation_input.text()
            gx = self.gx_input.text()
            x = np.linspace(-5, 5, 1000)

            # Define allowed functions and constants
            allowed_functions = {
                "sin": math.sin,
                "cos": math.cos,
                "log": math.log,
                "log10": math.log10,
                "tan": math.tan,
                "sqrt": math.sqrt,
                "pi": math.pi,
                "e": math.e
            }

            self.figure.clear()
            ax = self.figure.add_subplot(111)
            ax.axhline(0, color="black", linewidth=0.5, linestyle="--")  # Horizontal axis
            ax.axvline(0, color="black", linewidth=0.5, linestyle="--")  # Vertical axis

            if self.dropdown.currentIndex() == 2:
                y = np.array([eval(gx, {"x": val, **allowed_functions}) for val in x])
                ax.plot(x, y, label="g(x)")
                ax.plot(x, x, label="y=x", color="red")  # Plot y = x
            else:
                y = np.array([eval(equation, {"x": val, **allowed_functions}) for val in x])
                ax.plot(x, y, label="f(x)")

            ax.set_title("Graph of Equation")
            ax.set_xlabel("x")
            ax.set_ylabel("y")
            ax.legend()
            self.canvas.draw()

        except Exception as e:
            print(f"Error plotting graph: {e}")


    def get_root(self):
        data = self.get_data()
        if (self.validate(data)):
            (results, steps) = self.solve(data)
            self.open_result_window(results)
            self.open_steps_window(steps)

    def validate(self, data):
        idx = self.dropdown.currentIndex()
        if (data['equation'] == "" and idx != 2):
            self.error_label.setText("Enter the equation")
            self.error_label.show()
            return False
        
        if idx == 2 and data['gx_equation'] == "":
            self.error_label.setText("Enter the G(x) equation")
            self.error_label.show()
            return False

        if not str(data['max_itr']).isdigit() or int(data['max_itr']) <= 0:
            self.error_label.setText("Maximum iterations must be a positive number")
            self.error_label.show()
            return False
        
        try:
            tolerance = float(data['tolerance'])
            if tolerance <= 0 or tolerance > 100:
                self.error_label.setText("Tolerance must be a positive number not greater than 100")
                self.error_label.show()
                return False
        except ValueError:
            self.error_label.setText("Tolerance must be a valid number")
            self.error_label.show()
            return False
        
        if idx == 0 or idx == 1:
            try:
                low_bound = float(data['low_bound'])
                high_bound = float(data['high_bound'])
                if (high_bound <= low_bound):
                    self.error_label.setText("Invalid Low and High bounds")
                    self.error_label.show()
                    return False
            except ValueError:
                self.error_label.setText("Low bound and High bound must be valid numbers")
                self.error_label.show()
                return False
            
        if not str(data['significant_figures']).isdigit() or int(data['significant_figures']) <= 0:
            self.error_label.setText("Significant figures must be a positive number")
            self.error_label.show()
            return False
        
        if idx in [2,3,4]:
            if data['intial_guess'] == "":
                self.error_label.setText("Enter Intial Guess")
                self.error_label.show()
                return False            
            try:
                float(data['intial_guess'])
            except ValueError:
                self.error_label.setText("Intial Guess must be a number")
                self.error_label.show()
                return False
        
        if idx == 5:
            if data['secant_p1'] == "":
                self.error_label.setText("Enter P1")
                self.error_label.show()
                return False
            elif data['secant_p2'] == "":
                self.error_label.setText("Enter P2")
                self.error_label.show()
                return False
            try:
                float(data['secant_p1'])
            except ValueError:
                self.error_label.setText("P1 should be a number")
                self.error_label.show()
                return False
            try:
                float(data['secant_p2'])
            except ValueError:
                self.error_label.setText("P2 should be a number")
                self.error_label.show()
                return False

        # If all validations pass
        self.error_label.hide()

        return True

    def get_data(self):
        data = {}
        data['equation'] = self.equation_input.text()
        data['gx_equation'] = self.gx_input.text()

        data['significant_figures'] = self.sig_fig_input.text()
        if (data['significant_figures'] == ""):
            data['significant_figures'] = 20

        data['max_itr'] = self.max_iter_input.text()
        if (data['max_itr'] == ""):
            data['max_itr'] = 50

        data['tolerance'] = self.tolerance_input.text()
        if (data['tolerance'] == ""):
            data['tolerance'] = 0.00001

        data['low_bound'] = self.low_input.text()
        data['high_bound'] = self.high_input.text()
        data['intial_guess'] = self.intial_guess_input.text()
        data['secant_p1'] = self.secant_p1_input.text()
        data['secant_p2'] = self.secant_p2_input.text()
        return data

    def solve(self, data):
        print("get root pressed")
        match self.dropdown.currentIndex():
            case 0:
                return self.solver.bisection_method()
            case 1:
                return self.solver.bisection_method()
            case 2:
                return self.solver.bisection_method()
            case 3:
                return self.solver.bisection_method()
            case 4:
                return self.solver.bisection_method()
            case 5:
                return self.solver.bisection_method()
        # match self.dropdown.currentIndex():
        #     case 0:
        #         return self.solver.bisection_method()
        #     case 1:
        #         return self.solver.false_position_method()
        #     case 2:
        #         return self.solver.fixed_point_method()
        #     case 3:
        #         return self.solver.original_newton_raphson_method()
        #     case 4:
        #         return self.solver.modified_newton_raphson_method()
        #     case 5:
        #         return self.solver.secant_method()

    def open_result_window(self, results):
        try:
            self.result_window = ResultWindow(results)
            self.result_window.show()
            
        except Exception as e:
            print(f"Error opening result window: {e}")

    def open_steps_window(self, steps):
        try:
            self.table_window = TableWindow(steps)
            self.table_window.show()
        except Exception as e:
            print(f"Error opening steps window: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
