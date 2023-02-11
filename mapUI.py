from PyQt5 import QtCore
from PyQt5.QtWidgets import QPushButton, QLineEdit, QLabel, QCheckBox


class Ui_MapWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setGeometry(700, 300, 600, 620)
        MainWindow.setWindowTitle('Карты')

        self.map_label = QLabel(self)
        self.map_label.resize(600, 450)

        self.map_button = QPushButton(self)
        self.map_button.move(5, 455)
        self.map_button.setText("Карта")
        self.map_button.resize(190, 50)

        self.map_button.setFocusPolicy(QtCore.Qt.NoFocus)

        self.satellite = QPushButton(self)
        self.satellite.move(205, 455)
        self.satellite.setText("Спутник")
        self.satellite.resize(190, 50)

        self.satellite.setFocusPolicy(QtCore.Qt.NoFocus)

        self.hybrid = QPushButton(self)
        self.hybrid.move(405, 455)
        self.hybrid.setText("Гибрид")
        self.hybrid.resize(190, 50)

        self.hybrid.setFocusPolicy(QtCore.Qt.NoFocus)

        self.input_object = QLineEdit(self)
        self.input_object.move(5, 510)
        self.input_object.resize(400, 30)
        self.input_object.setEnabled(False)

        self.search_btn = QPushButton(self)
        self.search_btn.move(410, 510)
        self.search_btn.resize(185, 30)
        self.search_btn.setText("Найти")
        self.search_btn.setFocusPolicy(QtCore.Qt.NoFocus)

        self.reset_point_btn = QPushButton(self)
        self.reset_point_btn.move(5, 545)
        self.reset_point_btn.resize(590, 30)
        self.reset_point_btn.setText("Сброс метки")
        self.reset_point_btn.setFocusPolicy(QtCore.Qt.NoFocus)

        self.address_view = QLabel(self)
        self.address_view.move(5, 580)
        self.address_view.resize(600, 15)
        self.address_view.setText("")

        self.post_checkbox = QCheckBox(self)
        self.post_checkbox.move(5, 600)

        self.postindex_label = QLabel(self)
        self.postindex_label.move(25, 600)
        self.postindex_label.setText("Отображать почтовый индекс (если есть)")

        self.error_label = QLabel(self)
        self.error_label.move(300, 600)
        self.error_label.setText("")
        self.error_label.resize(500, 12)