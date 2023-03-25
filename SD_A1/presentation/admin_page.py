from PyQt5.QtCore import Qt, QDate
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QDateEdit, QSpinBox, QDialogButtonBox, QDialog, QPushButton, QTableWidget, QTableWidgetItem, QFileDialog, QMessageBox, QLineEdit

from model.user import User
from model.show import Show
from model.show_repository import ShowRepository
from model.user_repository import UserRepository
from logic.controller import Controller

import csv
import sys

from datetime import datetime

class AdminPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Call the Controller
        self.controller = Controller()

        # Create the main layout
        main_layout = QVBoxLayout()

        # Create the table widget for the shows
        self.show_table_widget = QTableWidget()
        self.show_table_widget.setColumnCount(5)
        self.show_table_widget.setHorizontalHeaderLabels(['Name', 'Singer', 'Date', 'Num Tickets', 'Genre'])
        self.show_table_widget.horizontalHeader().setStretchLastSection(True)
        # self.show_repo = ShowRepository()

        # Create the layout for the buttons
        show_button_layout = QHBoxLayout()

        # Create the 'delete show' button
        self.delete_show_button = QPushButton('Delete Show')
        show_button_layout.addWidget(self.delete_show_button)

        # Create the 'export shows' button
        self.export_shows_button = QPushButton('Export Shows')
        show_button_layout.addWidget(self.export_shows_button)

        # Create the 'add show' button
        self.add_show_button = QPushButton('Add Show')
        show_button_layout.addWidget(self.add_show_button)

        # Add the button layout to the main layout
        main_layout.addLayout(show_button_layout)

        # Add the table widget to the main layout
        main_layout.addWidget(self.show_table_widget)

        # Set the main layout
        self.setLayout(main_layout)

        # Connect the 'delete show' button to its handler
        self.delete_show_button.clicked.connect(self.delete_show)

        # Connect the 'export shows' button to its handler
        self.export_shows_button.clicked.connect(self.export_shows)

        # Connect the 'add show' button to its handler
        self.add_show_button.clicked.connect(self.add_show)

        # Populate the table widget with the shows
        self.populate_show_table()

        # Create the table widget for the cashiers
        self.cashier_table_widget = QTableWidget()
        self.cashier_table_widget.setColumnCount(2)
        self.cashier_table_widget.setHorizontalHeaderLabels(['Username', 'Name'])
        self.cashier_table_widget.horizontalHeader().setStretchLastSection(True)
        # self.user_repo = UserRepository()

        # Create the layout for the buttons
        cashier_button_layout = QHBoxLayout()

        # Create the 'delete cashier' button
        self.delete_cashier_button = QPushButton('Delete Cashier')
        cashier_button_layout.addWidget(self.delete_cashier_button)

        # Add the button layout to the main layout
        main_layout.addLayout(cashier_button_layout)

        # Add the table widget to the main layout
        main_layout.addWidget(self.cashier_table_widget)

        # Connect the 'delete cashier' button to its handler
        self.delete_cashier_button.clicked.connect(self.delete_cashier)

        # Populate the table widget with the cashiers
        self.populate_cashier_table()

    def populate_cashier_table(self):
        # Get all the cashiers
        cashiers = self.controller.get_all_cashiers()

        # Set the row count of the table widget
        self.cashier_table_widget.setRowCount(len(cashiers))

        # Populate the table widget with the cashiers
        for i, cashier in enumerate(cashiers):
            username_item = QTableWidgetItem(cashier.username)
            self.cashier_table_widget.setItem(i, 0, username_item)

    def populate_show_table(self):
        shows = self.controller.get_all_shows()
        self.show_table_widget.setRowCount(len(shows))
        for row, show in enumerate(shows):
            name_item = QTableWidgetItem(show.name)
            singer_item = QTableWidgetItem(show.singer)
            date_item = QTableWidgetItem(datetime.strptime(show.date, '%Y-%m-%d').strftime('%d/%m/%Y'))
            num_tickets_item = QTableWidgetItem(str(show.num_tickets))
            genre_item = QTableWidgetItem(show.genre)
            self.show_table_widget.setItem(row, 0, name_item)
            self.show_table_widget.setItem(row, 1, singer_item)
            self.show_table_widget.setItem(row, 2, date_item)
            self.show_table_widget.setItem(row, 3, num_tickets_item)
            self.show_table_widget.setItem(row, 4, genre_item)


    def add_show(self):
        # Create a QDialog for the add show form
        dialog = QDialog(self)
        dialog.setWindowTitle('Add Show')
        dialog.setWindowModality(Qt.ApplicationModal)

        # Create the form layout
        form_layout = QFormLayout()

        # Create the line edit widgets for the show form
        name_edit = QLineEdit()
        form_layout.addRow('Name:', name_edit)

        singer_edit = QLineEdit()
        form_layout.addRow('Singer:', singer_edit)

        date_edit = QDateEdit()
        date_edit.setDate(QDate.currentDate())
        form_layout.addRow('Date:', date_edit)

        num_tickets_edit = QSpinBox()
        num_tickets_edit.setMinimum(1)
        num_tickets_edit.setMaximum(1000)
        form_layout.addRow('Number of Tickets:', num_tickets_edit)

        genre_edit = QLineEdit()
        form_layout.addRow('Genre:', genre_edit)

        # Create the button box
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        form_layout.addWidget(button_box)

        # Create the signal connections for the button box
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)

        # Set the layout for the dialog
        dialog.setLayout(form_layout)

        # Show the dialog and wait for user input
        if dialog.exec() == QDialog.Accepted:
            # Get the form values
            name = name_edit.text()
            singer = singer_edit.text()
            date = date_edit.date().toPyDate()
            num_tickets = num_tickets_edit.value()
            genre = genre_edit.text()

            # Add the show data to the show repository
            self.controller.add_show(name, singer, date, num_tickets, genre)

            # Refresh the table widget
            self.populate_show_table()

    def delete_show(self):
        # Get the currently selected row
        selected_row = self.show_table_widget.currentRow()

        if selected_row != -1:
            # Get the show for the selected row
            show = self.controller.get_all_shows()[selected_row]

            # Delete the show from the repository
            self.controller.delete_show(show.name)

            # Refresh the table widget
            self.populate_show_table()

    def delete_cashier(self):
        # Get the currently selected row
        selected_row = self.cashier_table_widget.currentRow()

        if selected_row != -1:
            # Get the cashier for the selected row
            cashier = self.controller.get_all_cashiers()[selected_row]

            # Delete the cashier
            self.controller.delete_user(cashier.username)

            # Refresh the table widget
            self.populate_cashier_table()


    def export_shows(self):
        # Get all the shows
        shows = self.controller.get_all_shows()

        # Open a file dialog to get the path to save the file
        file_path, _ = QFileDialog.getSaveFileName(self, "Export Shows", "", "CSV Files (*.csv)")

        if file_path:
            # Write the shows to a CSV file
            with open(file_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Name', 'Singer', 'Date', 'Number of Tickets', 'Genre'])
                for show in shows:
                    date_obj = datetime.strptime(show.date, '%Y-%m-%d')
                    date_str = date_obj.strftime('%d/%m/%Y')
                    writer.writerow([show.name, show.singer, date_str, show.num_tickets, show.genre])

