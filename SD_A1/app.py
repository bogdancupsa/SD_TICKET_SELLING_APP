from PyQt5 import QtWidgets
from presentation.main_page import MainPage
import sys

# main function where the MainPage is displayed
if __name__ == '__main__':
    
    app = QtWidgets.QApplication(sys.argv)
    main_page = MainPage()
    main_page.show()

    sys.exit(app.exec_())
