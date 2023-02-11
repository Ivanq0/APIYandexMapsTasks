import sys


import requests
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget
from mapUI import Ui_MapWindow


class Example(QWidget, Ui_MapWindow):
    def __init__(self):
        super().__init__()
        self.lon = "73.299463"
        self.lat = "54.991783"
        self.zoom = "17"
        self.step_horz = 0.25
        self.step_vert = 0.25
        self.type = "map"
        self.point = ""
        self.address = ""
        self.postal_code = ""
        self.postal_flag = False

        self.setupUi(self)
        self.pixmap = QPixmap(self.draw_map())
        self.map_label.setPixmap(self.pixmap)

        self.map_button.clicked.connect(self.change_type)
        self.satellite.clicked.connect(self.change_type)
        self.hybrid.clicked.connect(self.change_type)
        self.search_btn.clicked.connect(self.search_object)
        self.reset_point_btn.clicked.connect(self.reset_object)
        self.post_checkbox.clicked.connect(self.show_postalindex)

    def search_object(self):
        if self.input_object.isEnabled():
            try:
                object = self.input_object.text().split("+")
                geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

                geocoder_params = {
                    "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
                    "geocode": object,
                    "format": "json"}

                response = requests.get(geocoder_api_server, params=geocoder_params)
                response_json = response.json()
                toponym = response_json["response"]["GeoObjectCollection"]["featureMember"][0]
                point = toponym["GeoObject"]["Point"]["pos"].split()
                data = toponym["GeoObject"]["metaDataProperty"]["GeocoderMetaData"]
                self.address = data["text"]
                if "postal_code" in data["Address"]:
                    self.postal_code = data["Address"]["postal_code"]
                    self.postal_flag = True
                else:
                    self.postal_flag = False
                if self.post_checkbox.isChecked() and self.postal_flag:
                    self.address_view.setText(f"{self.address}  |  Почтовый индекс: {self.postal_code}")
                else:
                    self.address_view.setText(self.address)
                self.lon = point[0]
                self.lat = point[1]
                self.point = f"{point[0]},{point[1]},flag"
                self.refresh_map()
                self.input_object.setEnabled(False)
                self.error_label.setText("")
            except Exception:
                self.error_label.setText("Объект не найден")
        else:
            self.input_object.setEnabled(True)

    def reset_object(self):
        self.point = ""
        self.address_view.setText("")
        self.address = ""
        self.postal_code = ""
        self.postal_flag = False
        self.refresh_map()

    def draw_map(self):
        api_server = "http://static-maps.yandex.ru/1.x/"
        params = {
            "ll": ",".join([self.lon, self.lat]),
            "z": self.zoom,
            "l": self.type,
            "pt": self.point
        }
        response = requests.get(api_server, params=params)
        map_file = "map.png"
        with open(map_file, "wb") as file:
            file.write(response.content)
        return map_file

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp:
            if int(self.zoom) + 1 <= 17:
                self.zoom = str(int(self.zoom) + 1)
                self.step_horz /= 2
                self.step_vert /= 2
        if event.key() == Qt.Key_PageDown:
            if int(self.zoom) - 1 >= 0:
                self.zoom = str(int(self.zoom) - 1)
                self.step_horz *= 2
                self.step_vert *= 2
        if event.key() == Qt.Key_Right:
            if (float(self.lon) + 0.0255 * self.step_horz) <= 180:
                self.lon = str(float(self.lon) + 0.0255 * self.step_horz)
        if event.key() == Qt.Key_Left:
            if (float(self.lon) - 0.0255 * self.step_horz) >= -180:
                self.lon = str(float(self.lon) - 0.0255 * self.step_horz)
        if event.key() == Qt.Key_Up:
            if (float(self.lat) + 0.0255 * self.step_vert) <= 90:
                self.lat = str(float(self.lat) + 0.0111 * self.step_vert)
        if event.key() == Qt.Key_Down:
            if (float(self.lat) - 0.0255 * self.step_vert) >= -90:
                self.lat = str(float(self.lat) - 0.0111 * self.step_vert)
        self.pixmap = QPixmap(self.draw_map())
        self.map_label.setPixmap(self.pixmap)

    def refresh_map(self):
        self.pixmap = QPixmap(self.draw_map())
        self.map_label.setPixmap(self.pixmap)

    def change_type(self):
        sender = self.sender()
        if sender.text() == "Карта":
            self.type = "map"
        if sender.text() == "Спутник":
            self.type = "sat"
        if sender.text() == "Гибрид":
            self.type = "sat,skl"
        self.refresh_map()

    def show_postalindex(self):
        if self.post_checkbox.isChecked() and self.postal_flag:
            self.address_view.setText(f"{self.address}  |  Почтовый индекс: {self.postal_code}")
        else:
            self.address_view.setText(self.address)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
