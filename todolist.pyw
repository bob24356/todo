import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
import pocket
#import model and pocket

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('favicon.ico'))
    todo = pocket.ToDo()
    todo.show()
    sys.exit(app.exec())
#RUN
