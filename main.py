# ***************************************************************************
#
# Author: Paul Littrell
# Lab:    CIS-133Y Lab 9
# Date:   November 20, 2026
# Desc:   Main GUI driver for the US Census Name Popularity Browser. Uses
#         PyGubu and Tkinter to query and display year-by-year name popularity
#         and percentage share.
#
# Input:  First name and gender selection.
# Output: Scrollable Treeview table showing Name, Year, Gender, NameCount,
#         Total yearly births, and added Popularity %.
# Source: Module 9 Lab 9
#
# ***************************************************************************

import os
import tkinter as tk
from tkinter import messagebox
import pygubu

import Name as n
import valid as v


PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
PROJECT_UI = os.path.join(PROJECT_PATH, "name_browser.ui")


class NameBrowserApp:
    """Controller class for the US Census Name Popularity Browser GUI."""

    def __init__(self, hidden_root):
        self.hidden_root = hidden_root

        # Initialize PyGubu builder
        self.builder = pygubu.Builder()
        self.builder.add_resource_path(PROJECT_PATH)
        self.builder.add_from_file(PROJECT_UI)

        # Build the main Toplevel window
        self.main_window = self.builder.get_object("main_window", self.hidden_root)

        # Ensure closing the Toplevel window terminates application
        self.main_window.protocol("WM_DELETE_WINDOW", self.on_close_window)

        # Retrieve widget references
        self.name_entry = self.builder.get_object("name_entry")
        self.results_treeview = self.builder.get_object("results_treeview")
        self.results_scrollbar = self.builder.get_object("results_scrollbar")
        self.status_label = self.builder.get_object("status_label")

        self.gender_var = self.builder.get_variable("gender_var")
        self.gender_var.set("M")

        self.results_treeview.configure(yscrollcommand=self.results_scrollbar.set)
        self.results_scrollbar.configure(command=self.results_treeview.yview)

        self.builder.connect_callbacks(self)

        # Allow pressing Enter inside the name Entry box to trigger a search
        self.name_entry.bind("<Return>", self.on_search_clicked)
        self.name_entry.focus_set()

    def clear_table(self):
        """Removes all existing rows from the results Treeview."""
        for item_id in self.results_treeview.get_children():
            self.results_treeview.delete(item_id)

    def populate_results_table(self, popularity_records):
        """Inserts Name objects into the Treeview with formatted counts and percentages."""
        self.clear_table()

        for record in popularity_records:
            row_values = (
                record.get_name(),
                record.get_year(),
                record.get_gender(),
                f"{record.get_count():,}",
                f"{record.get_total():,}",
                f"{record.get_popularity_percentage():.2f}%",
            )
            self.results_treeview.insert("", tk.END, values=row_values)

    def on_search_clicked(self, _event=None):
        """Validates user input, queries the database, and displays results."""
        raw_name = self.name_entry.get()
        raw_gender = self.gender_var.get()

        # Validate first name
        is_name_valid, name_result = v.validate_name(raw_name)
        if not is_name_valid:
            messagebox.showwarning("Invalid Name Input", name_result, parent=self.main_window)
            self.name_entry.focus_set()
            return

        # Validate gender selection
        is_gender_valid, gender_result = v.validate_gender(raw_gender)
        if not is_gender_valid:
            messagebox.showwarning("Invalid Gender Selection", gender_result, parent=self.main_window)
            return

        self.status_label.configure(
            text=f"Searching census records for '{name_result}' ({gender_result})..."
        )
        self.main_window.update_idletasks()

        try:
            records = n.Name.get_name_popularity(name_result, gender_result)
        except Exception as db_error:
            messagebox.showerror(
                "Database Connection Error",
                f"Unable to fetch records from the database:\n{db_error}",
                parent=self.main_window,
            )
            self.status_label.configure(text="Database error occurred.")
            return

        if not records:
            self.clear_table()
            self.status_label.configure(
                text=f"No records found for '{name_result}' ({gender_result})."
            )
            messagebox.showinfo(
                "No Results Found",
                f"No census records matched '{name_result}' with gender '{gender_result}'.",
                parent=self.main_window,
            )
            return

        self.populate_results_table(records)
        self.status_label.configure(
            text=f"Showing {len(records)} yearly records for '{name_result}' ({gender_result})."
        )

    def on_clear_clicked(self):
        """Resets inputs, clears the Treeview, and restores the default status."""
        self.name_entry.delete(0, tk.END)
        self.gender_var.set("M")
        self.clear_table()
        self.status_label.configure(text="Ready. Enter a name and select M or F to begin.")
        self.name_entry.focus_set()

    def on_close_window(self):
        """Cleanly destroys the hidden Tk root when the Toplevel window closes."""
        self.hidden_root.destroy()

    def run(self):
        """Starts the Tkinter main event loop."""
        self.hidden_root.mainloop()


def main():
    # Create default Tkroot
    hidden_root = tk.Tk()
    hidden_root.withdraw()

    app = NameBrowserApp(hidden_root)
    app.run()


if __name__ == "__main__":
    main()