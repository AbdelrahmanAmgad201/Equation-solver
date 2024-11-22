

class Parser:
    def __init__(self):
        # AX = B
        self.matrixA = None  # Placeholder for coefficient matrix (A)
        self.matrixB = None  # Placeholder for matrix (B)

    def get_input(self, equation_string):
        """
        Parses the input equation string and prepares it for processing.
        Args:
            equation_string (str): The equation string to be parsed.
        """
        pass

    def parse_coefficients(self, equation_string):
        """
        Extracts the coefficients from the equation string and forms matrixA.
        Args:
            equation_string (str): The equation string containing the coefficients.
        """
        pass

    def parse_constants(self, equation_string):
        """
        Extracts the constants from the equation string and forms matrixB.
        Args:
            equation_string (str): The equation string containing the constants.
        """
        pass

    def validate_input(self, equation_string):
        """
        Validates the input equation string to ensure it is in the correct format.
        Args:
            equation_string (str): The input equation string.
        Returns:
            bool: True if the input is valid, False otherwise.
        """
        pass

