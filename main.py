import sys
from PyQt6.QtWidgets import QApplication
from view.home_ui import HomeWindow  # importa la tua classe HomeWindow

def main():
    app = QApplication(sys.argv)
    window = HomeWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()