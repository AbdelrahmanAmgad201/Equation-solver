import tkinter as tk
from tkinter import messagebox
import pprint
from PIL import Image, ImageTk


class MatrixDelegator:

    def __init__(self, main_frame, matrix_frame, size):
        self.matrix_frame = matrix_frame
        self.main_frame = main_frame
        self.size = size
        self.is_matrix_ready = False

        self.text_widget = tk.Text(self.main_frame, wrap=tk.WORD, width=50, height=15)
        self.text_widget.pack(pady=10)


        self.output_matrix = [[None for _ in range(self.size)] for _ in range(self.size)]

        self.all_entries = []
        self.place_holders = []

        self.create_entries()

        self.confirm_matrix = tk.Button(self.matrix_frame, text="Confirm", command=self.create_matrix)
        self.confirm_matrix.grid(columnspan=self.size)

        self.back_button = tk.Button(self.matrix_frame, text="Home Page", command=self.go_to_home_page)
        self.back_button.grid(columnspan=self.size)

        # Button to display the pprint output of the matrix

    def create_entries(self):
        for i in range(self.size):
            for j in range(self.size +1):
                place_holder = f'A{i}{j}'
                
                if j == self.size:
                    place_holder = f'B{i}'
                    
                entry = tk.Entry(self.matrix_frame, fg='gray')
                entry.insert(0, place_holder)
                entry.grid(row=i, column=j, pady=5)

                entry.bind("<FocusIn>", lambda event, ph=place_holder: self.on_focus_in(event, ph))
                entry.bind("<FocusOut>", lambda event, ph=place_holder: self.on_focus_out(event, ph))

                self.all_entries.append(entry)
                self.place_holders.append(place_holder)
            self.matrix_frame.grid_columnconfigure(i, weight=1)

    
    def create_matrix(self):
        """Convert entries into a matrix, returns back to Home page if input is correct."""
        self.is_matrix_ready = True

        for index in range(self.size * (self.size + 1)):
            entry = self.all_entries[index].get().strip()  # Get and trim the entry

            # Determine the row and column of the entry
            row = index // (self.size + 1)
            col = index % (self.size + 1)

            # Handle placeholder checks
            if entry == self.place_holders[index] or entry == "":
                self.is_matrix_ready = False
                self.all_entries[index].config(bg='red')
            else:
                self.all_entries[index].config(bg='white')

                # Handle the last column (B{j})
                if col == self.size:
                    self.output_matrix[row].append(entry)  # For B{j}, append to the row (or handle as necessary)
                else:
                    self.output_matrix[row][col] = entry  # For other columns, assign directly

        if not self.is_matrix_ready:
            messagebox.showerror("ERROR!", f"Invalid input!")
        else:
            self.draw_input_matrix()  # Now calls draw_input_matrix() after matrix creation
            self.go_to_home_page()


    def draw_input_matrix(self):
        """Display the input matrix in a formatted way using pprint."""
        matrix = self.get_matrix()

        # Temporarily enable the Text widget to insert content
        self.text_widget.config(state=tk.NORMAL)
        self.text_widget.delete("1.0", tk.END)  # Clear existing content

        if matrix is not None:
            formatted_matrix = pprint.pformat(matrix)
        else:
            formatted_matrix = "Matrix is not ready yet."

        # Insert the formatted matrix into the Text widget
        self.text_widget.insert(tk.END, f"Input Matrix:\n{formatted_matrix}\n")
        
        # Disable the Text widget to prevent typing
        self.text_widget.config(state=tk.DISABLED)



    def draw_output_matrix(self, matrices):
        """
        Display the output matrices in a TopLevel window with Next and Previous buttons.
        The matrices parameter is a list of matrices.
        """
        if not matrices or not isinstance(matrices, list):
            messagebox.showerror("Error", "No matrices to display!")
            return

        # Initialize the index tracker for the current matrix
        self.current_matrix_index = 0

        def update_matrix_display():
            """Update the matrix display in the Text widget."""
            self.matrix_display_text.config(state=tk.NORMAL)  # Enable the widget
            self.matrix_display_text.delete("1.0", tk.END)  # Clear existing content
            formatted_matrix = pprint.pformat(matrices[self.current_matrix_index])
            self.matrix_display_text.insert(tk.END, f"Output Matrix ({self.current_matrix_index + 1}/{len(matrices)}):\n{formatted_matrix}")
            self.matrix_display_text.config(state=tk.DISABLED)  # Disable the widget

        def next_matrix():
            """Display the next matrix in the list."""
            if self.current_matrix_index < len(matrices) - 1:
                self.current_matrix_index += 1
                update_matrix_display()

        def previous_matrix():
            """Display the previous matrix in the list."""
            if self.current_matrix_index > 0:
                self.current_matrix_index -= 1
                update_matrix_display()

        # Create a TopLevel window
        matrix_window = tk.Toplevel(self.main_frame)
        matrix_window.title("Output Matrices")

        # Add a Text widget for displaying the matrix
        self.matrix_display_text = tk.Text(matrix_window, wrap=tk.WORD, width=50, height=15, state=tk.DISABLED)
        self.matrix_display_text.pack(pady=10)

        # Add "Previous" and "Next" buttons
        button_frame = tk.Frame(matrix_window)
        button_frame.pack(pady=5)

        prev_button = tk.Button(button_frame, text="Previous", command=previous_matrix)
        prev_button.pack(side=tk.LEFT, padx=5)

        next_button = tk.Button(button_frame, text="Next", command=next_matrix)
        next_button.pack(side=tk.RIGHT, padx=5)

        # Display the first matrix initially
        update_matrix_display()




    def go_to_home_page(self):
        # Hide the matrix frame
        self.matrix_frame.pack_forget()

        # Show the main frame again
        self.main_frame.pack(fill='both', expand=True)

    def on_focus_in(self, event, placeholder):
        """Clear the placeholder text when the entry widget is focused."""
        entry = event.widget
        if entry.get() == placeholder:
            entry.delete(0, tk.END)
            entry.config(fg='black')

    def on_focus_out(self, event, placeholder):
        """Set the placeholder text if the entry is empty."""
        entry = event.widget
        if entry.get() == '':
            entry.insert(0, placeholder)
            entry.config(fg='gray')

    def get_matrix(self):
        if self.is_matrix_ready:
            return self.output_matrix
        else:
            return None

