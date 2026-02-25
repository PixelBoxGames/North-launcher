from PyQt6 import QtWidgets, uic
import sys, webbrowser, json

class InfoDialog(QtWidgets.QDialog):
    def __init__(self, parent = None):
        super().__init__(parent)
        uic.loadUi('info.ui', self)

class VerDialog(QtWidgets.QDialog):
    def __init__(self, parent = None):
        super().__init__(parent)
        uic.loadUi('ver_create.ui', self)

class CreateAccountDialog(QtWidgets.QDialog):
    def __init__(self, parent = None):
        super().__init__(parent)
        uic.loadUi('account_create.ui', self)

class SettingsDialog(QtWidgets.QDialog):
    def __init__(self, parent = None):
        super().__init__(parent)
        uic.loadUi('settings.ui', self)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.info_btn.clicked.connect(self.open_info)
        self.settings_btn.clicked.connect(self.open_settings)
        self.add_account_btn.clicked.connect(self.create_account)
        self.add_btn.clicked.connect(self.create_version)
        self.links_btn.clicked.connect(self.open_links)

    def open_info(self):
        self.dialog = InfoDialog(self)
        self.dialog.exec()

    def open_settings(self):
        self.dialog = SettingsDialog(self)
        with open('launch-settings.json', "r") as json_file:
            settings_string = json.load(json_file)
        self.dialog.ram_select.setCurrentText(str(settings_string["ram"]))

        result = self.dialog.exec()
        if result == self.dialog.accepted:
            with open('launch-settings.json', "w") as json_file:
                json.dump(f, json_file, indent=4)


    def create_account(self):
        self.dialog = CreateAccountDialog(self)
        self.dialog.exec()

    def create_version(self):
        self.dialog = CreateAccountDialog(self)
        self.dialog.exec()

    def open_links(self):
        webbrowser.open_new_tab('https://t.me/NorthLauncher')


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
