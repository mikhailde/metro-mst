import sys
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QSizePolicy,
)

from gui.main_window import DrawingArea
from algorithms.mst import MetroOptimizer

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Оптимизатор сети метро")
        self.setGeometry(100, 100, 800, 600)

        self.metro_optimizer = MetroOptimizer()
        self.drawing_area = DrawingArea(self)

        self.setStyleSheet(
            """
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 8px 16px;
                text-align: center;
                font-size: 16px;
                margin: 4px 2px;
                border-radius: 4px;
            }

            QPushButton:hover {
                background-color: #45a049;
            }

            QLabel {
                font-size: 14px;
                color: #333;
            }

            QStatusBar {
                font-size: 12px;
            }

            QStatusBar QLabel { 
                color: white; 
            }
        """
        )

        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        self.setCentralWidget(central_widget)

        button_layout = QHBoxLayout()
        layout.addLayout(button_layout)

        clear_button = QPushButton("Очистить", self)
        clear_button.clicked.connect(self.clear_stations)
        button_layout.addWidget(clear_button)

        self.drawing_area.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        layout.addWidget(self.drawing_area)

        self.status_label = QLabel("Левая кнопка - добавить/переместить, Правая - удалить, Средняя - панорамировать", self)
        self.statusBar().addWidget(self.status_label)

    def clear_stations(self):
        self.metro_optimizer.stations = []
        self.drawing_area.update()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())