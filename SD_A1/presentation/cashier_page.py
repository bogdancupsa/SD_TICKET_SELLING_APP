from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem
from model.show import Show
from model.show_repository import ShowRepository
from logic.controller import Controller
import sys
from datetime import datetime

class CashierPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Add the controller
        self.controller = Controller()

        # Create the main layout
        main_layout = QVBoxLayout()

        # self.show_repo = ShowRepository()

        # Create the table widget for the shows
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(5)
        self.table_widget.setHorizontalHeaderLabels(['Name', 'Singer', 'Date', 'Available Tickets', 'Genre'])
        self.table_widget.horizontalHeader().setStretchLastSection(True)

        # Create the layout for the buttons
        button_layout = QHBoxLayout()

        # Create the 'sell ticket' button
        self.sell_ticket_button = QPushButton('Sell Ticket')
        button_layout.addWidget(self.sell_ticket_button)

        # Add the button layout to the main layout
        main_layout.addLayout(button_layout)

        # Add the table widget to the main layout
        main_layout.addWidget(self.table_widget)

        # Set the main layout
        self.setLayout(main_layout)

        # Connect the 'sell ticket' button to its handler
        self.sell_ticket_button.clicked.connect(self.sell_ticket)

        # Populate the table widget with the shows
        self.populate_table()

    def populate_table(self):
        # Get all the shows
        shows = self.controller.get_all_shows()

        # Set the row count of the table widget
        self.table_widget.setRowCount(len(shows))

        # Populate the table widget with the shows
        for i, show in enumerate(shows):
            name_item = QTableWidgetItem(show.name)
            singer_item = QTableWidgetItem(show.singer)
            date_obj = datetime.strptime(show.date, '%Y-%m-%d')
            date_item = QTableWidgetItem(date_obj.strftime('%d/%m/%Y'))
            available_tickets_item = QTableWidgetItem(str(show.num_tickets))
            genre_item = QTableWidgetItem(show.genre)
            self.table_widget.setItem(i, 0, name_item)
            self.table_widget.setItem(i, 1, singer_item)
            self.table_widget.setItem(i, 2, date_item)
            self.table_widget.setItem(i, 3, available_tickets_item)
            self.table_widget.setItem(i, 4, genre_item)

            # Add the 'sell ticket' button to the last column of the row
            sell_ticket_button = QPushButton('Sell Ticket')
            sell_ticket_button.clicked.connect(lambda _, show=show: self.sell_ticket_for_show(show))
            self.table_widget.setCellWidget(i, 5, sell_ticket_button)

    def sell_ticket_for_show(self, show):
        # Decrement the available tickets for the show
        if show.num_tickets >= 1:
            show.num_tickets -= 1

        # Update show with the new tickets number value
        self.controller.update_show(show.name, show.singer, show.date, show.num_tickets, show.genre)

        # Refresh the table widget
        self.populate_table()


    def sell_ticket(self):
        # Get the currently selected row
        selected_row = self.table_widget.currentRow()

        if selected_row != -1:
            # Get the show for the selected row
            show = self.controller.get_all_shows()[selected_row]

            # Sell a ticket for the show
            self.sell_ticket_for_show(show)
