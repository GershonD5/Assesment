import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import os
from data_processing import process_data
from logging_config import configure_logging

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Data Processing GUI")

        # Labels and buttons
        tk.Label(root, text="Select the folder containing transaction files (Year):").pack(pady=5)
        self.folder_button = tk.Button(root, text="Select Folder", command=self.select_folder)
        self.folder_button.pack(pady=5)
        self.folder_label = tk.Label(root, text="")
        self.folder_label.pack(pady=5)

        tk.Label(root, text="Select the exchange rate file:").pack(pady=5)
        self.file_button = tk.Button(root, text="Select File", command=self.select_file)
        self.file_button.pack(pady=5)
        self.file_label = tk.Label(root, text="")
        self.file_label.pack(pady=5)

        tk.Label(root, text="Select the output file:").pack(pady=5)
        self.output_button = tk.Button(root, text="Select Output File", command=self.select_output_file)
        self.output_button.pack(pady=5)
        self.output_file_label = tk.Label(root, text="")
        self.output_file_label.pack(pady=5)

        self.start_button = tk.Button(root, text="Start Processing", command=self.start_processing)
        self.start_button.pack(pady=20)

        self.close_button = tk.Button(root, text="Close", command=self.close_app)
        self.close_button.pack(pady=5)

        # Variables to store paths
        self.root_dir = ""
        self.exchange_rate_file = ""
        self.output_file = ""

        # Set up logging
        configure_logging()

    def select_folder(self):
        self.root_dir = filedialog.askdirectory(title="Select the folder containing transaction files")
        if self.root_dir:
            self.folder_label.config(text=f"Transaction folder: {self.root_dir}")

    def select_file(self):
        self.exchange_rate_file = filedialog.askopenfilename(
            title="Select the exchange rate file",
            filetypes=[("Excel files", "*.xlsx *.xls")]
        )
        if self.exchange_rate_file:
            self.file_label.config(text=f"Exchange rate file: {self.exchange_rate_file}")

    def select_output_file(self):
        self.output_file = filedialog.asksaveasfilename(
            title="Select Output File",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")]
        )
        if self.output_file:
            self.output_file_label.config(text=f"Output file: {self.output_file}")

    def start_processing(self):
        if not self.root_dir or not self.exchange_rate_file or not self.output_file:
            messagebox.showerror("Error", "Please select all required files and folders.")
            return

        result = process_data(self.root_dir, self.exchange_rate_file, self.output_file)
        
        if result:
            messagebox.showinfo(
                "Processing Complete",
                result
            )
        else:
            messagebox.showerror(
                "Processing Error",
                "An error occurred during processing. Please check the log file."
            )

    def close_app(self):
        self.root.destroy()
