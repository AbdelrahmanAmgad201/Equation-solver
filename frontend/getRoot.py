from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets

from PyQt5.QtWidgets import (
    QApplication, QLabel, QComboBox,
    QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton
)
import sys
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from .result_window import ResultWindow
from backend.nonlinear_equation.solver import Solver
from .steps import TableWindow
from sympy import symbols, sin, cos, exp, sympify, lambdify, N


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
                                "First Modified Newton-Raphson",
                                "Second Modified Newton-Raphson",
                                "Secant"])  # Add dropdown items
        self.dropdown.currentIndexChanged.connect(self.handle_dropdown_change)

        # Equation and G(x) inputs
        self.equation_label = QLabel("f(x)=")
        self.equation_input = QLineEdit()
        self.gx_label = QLabel("g(x)=")
        self.gx_input = QLineEdit()

        # Initially hide G(x) input
        self.gx_label.hide()
        self.gx_input.hide()

        self.plot_interval_label = QLabel("(x interval)")
        self.plot_x1_label = QLabel("x1:")
        self.plot_x1_input = QLineEdit()
        self.plot_x2_label = QLabel("x2:")
        self.plot_x2_input = QLineEdit()

        plot_interval_layout = QHBoxLayout()
        plot_interval_layout.addWidget(self.plot_interval_label)
        plot_interval_layout.addWidget(self.plot_x1_label)
        plot_interval_layout.addWidget(self.plot_x1_input)
        plot_interval_layout.addWidget(self.plot_x2_label)
        plot_interval_layout.addWidget(self.plot_x2_input)

        self.plot_fx_button = QPushButton("Plot f(x)")
        self.plot_fx_button.clicked.connect(self.plot_fx)

        self.plot_gx_button = QPushButton("Plot g(x)")
        self.plot_gx_button.clicked.connect(self.plot_gx)

        self.plot_gx_button.hide()

        plot_buttons_layout = QHBoxLayout()
        plot_buttons_layout.addWidget(self.plot_fx_button)
        plot_buttons_layout.addWidget(self.plot_gx_button)

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

        self.multiplicity_label = QLabel("Root Multiplicity:")
        self.multiplicity_input = QLineEdit()

        self.multiplicity_label.hide()
        self.multiplicity_input.hide()

        multiplicity_layout = QHBoxLayout()
        multiplicity_layout.addWidget(self.multiplicity_label)
        multiplicity_layout.addWidget(self.multiplicity_input)

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

        back_button_layout = QHBoxLayout()
        back_button_layout.addStretch(1)
        back_button_layout.addWidget(self.back_button)
        back_button_layout.addStretch(1)

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
        main_layout.addLayout(plot_interval_layout)
        main_layout.addLayout(plot_buttons_layout)
        main_layout.addWidget(self.canvas)
        main_layout.addLayout(sig_fig_layout)
        main_layout.addLayout(max_iter_layout)
        main_layout.addLayout(tolerance_layout)
        main_layout.addLayout(low_high_layout)
        main_layout.addLayout(intial_guess_layout)
        main_layout.addLayout(secant_intials_layout)
        main_layout.addLayout(multiplicity_layout)
        main_layout.addLayout(root_button_layout)
        main_layout.addLayout(back_button_layout)

    def handle_dropdown_change(self):
        self.hide_all_extra_input()
        method = self.dropdown.currentText()

        if method == "Bisection" or method == "False-Position":
            self.show_bisection_input()

        if method == "Fixed point":
            self.show_gx_input()

        if method in ["Fixed point", "Original Newton-Raphson", "First Modified Newton-Raphson",
                      "Second Modified Newton-Raphson"]:
            self.show_intial_guess()

        if method == "First Modified Newton-Raphson":
            self.show_multiplicity_input()

        if method == "Secant":
            self.show_intial_secant_input()

    def show_gx_input(self):
        self.gx_label.show()
        self.gx_input.show()
        self.plot_gx_button.show()

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

    def show_multiplicity_input(self):
        self.multiplicity_label.show()
        self.multiplicity_input.show()

    def hide_all_extra_input(self):
        self.gx_label.hide()
        self.gx_input.hide()
        self.plot_gx_button.hide()
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
        self.multiplicity_label.hide()
        self.multiplicity_input.hide()

    def validate_plot_interval(self):
        try:
            start_x = self.plot_x1_input.text()
            end_x = self.plot_x2_input.text()
            if start_x == "" and end_x == "":
                return -3, 3
            else:
                start_x = float(start_x)
                end_x = float(end_x)
                if (start_x == end_x):
                    print("interval start == interval end")
                    self.error_label.setText("Invalid Interval")
                    self.error_label.show()
                else:
                    if (end_x < start_x):
                        tmp = start_x
                        start_x = end_x
                        end_x = tmp
                    return start_x, end_x
        except Exception as e:
            print(e)
            self.error_label.setText("Invalid Interval")
            self.error_label.show()
            return

    def plot_fx(self):
        try:
            self.error_label.hide()
            start_x, end_x = self.validate_plot_interval()
            if (start_x == None):
                return
            x = np.linspace(start_x, end_x, 1000)
            self.figure.clear()
            ax = self.figure.add_subplot(111)
            ax.axhline(0, color="black", linewidth=0.5, linestyle="--")  # Horizontal axis
            ax.axvline(0, color="black", linewidth=0.5, linestyle="--")  # Vertical axis
            equation = self.equation_input.text()
            equation_lambda = self.string_to_lambda(equation, ["x"])
            y = np.array([equation_lambda(val) for val in x])
            ax.plot(x, y, label="f(x)")
            ax.set_title("Graph of F(x)")
            ax.set_xlabel("x")
            ax.set_ylabel("y")
            ax.legend()
            self.canvas.draw()

        except Exception as e:
            print(e)
            self.error_label.setText("Invalid Equation")
            self.error_label.show()

    def plot_gx(self):
        try:
            self.error_label.hide()
            start_x, end_x = self.validate_plot_interval()
            if (start_x == None):
                return
            x = np.linspace(start_x, end_x, 1000)
            self.figure.clear()
            ax = self.figure.add_subplot(111)
            ax.axhline(0, color="black", linewidth=0.5, linestyle="--")  # Horizontal axis
            ax.axvline(0, color="black", linewidth=0.5, linestyle="--")  # Vertical axis

            gx = self.gx_input.text()
            gx_lambda = self.string_to_lambda(gx, ["x"])
            y = np.array([gx_lambda(val) for val in x])
            ax.plot(x, y, label="g(x)")
            ax.plot(x, x, label="y=x", color="red")  # Plot y = x
            ax.set_title("Graph of g(x)")
            ax.set_xlabel("x")
            ax.set_ylabel("y")
            ax.legend()
            self.canvas.draw()

        except Exception as e:
            print(e)
            self.error_label.setText("Invalid g(x)")
            self.error_label.show()

    def get_root(self):
        data = self.get_data()
        data = self.validate(data)
        if (data != None):
            results, steps = self.solver.solve(data)
            self.open_result_window(results)
            self.open_steps_window(steps)

    def validate(self, data):
        method = self.dropdown.currentText()
        if (data['equation'] == "" and method != "Fixed point"):
            self.error_label.setText("Enter the equation")
            self.error_label.show()
            return None

        if method == "Fixed point" and data['gx_equation'] == "":
            self.error_label.setText("Enter the G(x) equation")
            self.error_label.show()
            return None

        if method == "Fixed point":
            try:
                gx = self.gx_input.text()
                data['gx_equation'] = self.string_to_lambda(gx, ["x"])
            except Exception as e:
                self.error_label.setText("Invalid G(x) equation")
                self.error_label.show()
                return None

        try:
            equation = self.equation_input.text()
            data['equation'] = self.string_to_lambda(equation, ["x"])
        except Exception as e:
            self.error_label.setText("Invalid F(x) equation")
            self.error_label.show()
            return None

        if not str(data['max_itr']).isdigit() or int(data['max_itr']) <= 0:
            self.error_label.setText("Maximum iterations must be a positive number")
            self.error_label.show()
            return None
        else:
            data['max_itr'] = int(data['max_itr'])

        try:
            data['tolerance'] = float(data['tolerance'])
            if data['tolerance'] <= 0 or data['tolerance'] > 100:
                self.error_label.setText("Tolerance must be a positive number not greater than 100")
                self.error_label.show()
                return None
        except ValueError:
            self.error_label.setText("Tolerance must be a valid number")
            self.error_label.show()
            return None

        if method == "Bisection" or method == "False-Position":
            try:
                data['low_bound'] = float(data['low_bound'])
                data['high_bound'] = float(data['high_bound'])
            except ValueError:
                self.error_label.setText("Low bound and High bound must be valid numbers")
                self.error_label.show()
                return None
        if data['significant_figures'] != None:
            if not str(data['significant_figures']).isdigit() or int(data['significant_figures']) <= 0:
                self.error_label.setText("Significant figures must be a positive number")
                self.error_label.show()
                return None
            else:
                data['significant_figures'] = int(data['significant_figures'])

        if method in ["Fixed point", "Original Newton-Raphson", "First Modified Newton-Raphson",
                      "Second Modified Newton-Raphson"]:
            if data['initial_guess'] == "":
                self.error_label.setText("Enter Intial Guess")
                self.error_label.show()
                return None
            try:
                data['initial_guess'] = float(data['initial_guess'])
            except ValueError:
                self.error_label.setText("Intial Guess must be a number")
                self.error_label.show()
                return None

        if method == "First Modified Newton-Raphson":
            if data['multiplicity'] == "":
                self.error_label.setText("Enter root multiplicity")
                self.error_label.show()
                return None
            else:
                try:
                    data['multiplicity'] = int(data['multiplicity'])
                except ValueError:
                    self.error_label.setText("Invalid Root Multiplicity")
                    self.error_label.show()
                    return None

        if method == "Secant":
            if data['secant_p1'] == "":
                self.error_label.setText("Enter P1")
                self.error_label.show()
                return None
            elif data['secant_p2'] == "":
                self.error_label.setText("Enter P2")
                self.error_label.show()
                return None
            try:
                data['secant_p1'] = float(data['secant_p1'])
            except ValueError:
                self.error_label.setText("P1 should be a number")
                self.error_label.show()
                return None
            try:
                data['secant_p2'] = float(data['secant_p2'])
            except ValueError:
                self.error_label.setText("P2 should be a number")
                self.error_label.show()
                return None

        # If all validations pass
        self.error_label.hide()
        return data

    def get_data(self):
        data = {}
        data['method'] = self.dropdown.currentText()
        data['equation'] = self.equation_input.text()
        data['gx_equation'] = self.gx_input.text()

        data['significant_figures'] = self.sig_fig_input.text()
        if (data['significant_figures'] == ""):
            data['significant_figures'] = None

        data['max_itr'] = self.max_iter_input.text()
        if (data['max_itr'] == ""):
            data['max_itr'] = 50

        data['tolerance'] = self.tolerance_input.text()
        if (data['tolerance'] == ""):
            data['tolerance'] = 0.00001

        data['low_bound'] = self.low_input.text()
        data['high_bound'] = self.high_input.text()
        data['initial_guess'] = self.intial_guess_input.text()
        data['secant_p1'] = self.secant_p1_input.text()
        data['secant_p2'] = self.secant_p2_input.text()
        data['multiplicity'] = self.multiplicity_input.text()
        return data

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

    def string_to_lambda(self, func_str, variables):
        """
        Converts a string function into a lambda function with sin, cos, and exp
        wrapped in N() for numerical evaluation.

        Parameters:
            func_str (str): The function as a string.
            variables (list): List of variables as strings (e.g., ["x", "y"]).

        Returns:
            lambda function: A lambda function ready for numerical evaluation.
        """
        # Define symbolic variables
        sym_vars = symbols(variables)
        func_expr = sympify(func_str, locals={"sin": lambda x: N(sin(x)),
                                              "cos": lambda x: N(cos(x)),
                                              "exp": lambda x: N(exp(x))})
        func_lambda = lambdify(sym_vars, func_expr)
        return func_lambda


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
