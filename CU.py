import frontend as fe
import backend as be
from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer
import time

import sys

class CU:
        _output= []
        _execution_time = 0

        def print_matrix(self):
            app = QtWidgets.QApplication(sys.argv)
            window = fe.MainWindow()
            the_input = []


            observer_timer = QTimer()
            observer_timer.timeout.connect(lambda: self._handle_timeout(window, the_input))
            observer_timer.start(100)

            sys.exit(app.exec_())

        def _handle_timeout(self, window, the_input):
            # Control logic
            the_input = fe.ckeck_observer.check_observer_out(window)
            self._control(the_input)
            fe.ckeck_observer.check_observer_in(window, self._output,self._execution_time)
        def _control(self,the_input):
            if the_input[0] == None or the_input[1] == None :
                return []
            try:
                parser = be.Parser(the_input[0],the_input[1]['scaled'])

                if the_input[1]['method'] == "Gauss":
                    solver = be.Gauss_Elimination(parser)
                    start_time = time.time()
                    self._output = solver.solve(sf=the_input[1]['significant_digits'])
                    end_time = time.time()
                    self._execution_time = end_time - start_time
                elif the_input[1]['method'] == "Jacobi":

                    solver = be.Jacobi_iteration(parser,error= the_input[1]['absolute_relative_error'],
                                             iterations=the_input[1]['iterations'],
                                             sf=the_input[1]['significant_digits'],
                                             initial=the_input[1]['initial_vector'])
                    start_time = time.time()
                    self._output = solver.solve()
                    end_time = time.time()
                    self._execution_time = end_time - start_time
                elif the_input[1]['method'] == "Crout":
                    solver = be.LU_Decomposition(parser)
                    start_time = time.time()
                    self._output = solver.solve_LU_Crout(sf=the_input[1]['significant_digits'])
                    end_time = time.time()
                    self._execution_time = end_time - start_time
                elif the_input[1]['method'] == "Dolittle":
                    solver = be.LU_Decomposition(parser)
                    start_time = time.time()
                    self._output = solver.solve_LU_Doolittle(sf=the_input[1]['significant_digits'])
                    end_time = time.time()
                    self._execution_time = end_time - start_time
                elif the_input[1]['method'] == "Cholesky":
                    solver = be.LU_Decomposition(parser)
                    start_time = time.time()
                    self._output = solver.solve_LU_Cholesky(sf=the_input[1]['significant_digits'])
                    end_time = time.time()
                    self._execution_time = end_time - start_time
                elif the_input[1]['method'] == "Gauss Jordan":
                    solver = be.Gauss_Jordan(parser)
                    start_time = time.time()
                    self._output = solver.solve(sf=the_input[1]['significant_digits'])
                    end_time = time.time()
                    self._execution_time = end_time - start_time
                elif the_input[1]['method'] == "Gauss Seidel":
                    solver = be.Gauss_Seidel(parser, error=the_input[1]['absolute_relative_error'],
                                             iterations=the_input[1]['iterations'],
                                             sf=the_input[1]['significant_digits'],
                                             initial=the_input[1]['initial_vector'])
                    start_time = time.time()
                    self._output = solver.solve()
                    end_time = time.time()
                    self._execution_time = end_time - start_time

            except Exception as e:
                print(e)
                self._output = None




















