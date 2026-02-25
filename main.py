from PyQt6 import QtWidgets, uic
import sys, webbrowser, json
import minecraft_launcher_lib as mlib

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
        self.github_btn.clicked.connect(self.open_github)

    def open_info(self):
        self.dialog = InfoDialog(self)
        self.dialog.exec()

    def open_settings(self):
        self.dialog = SettingsDialog(self)
        with open('launch-settings.json', "r") as json_file:
            settings_string = json.load(json_file)
        self.dialog.ram_select.setCurrentText(str(settings_string["ram"]))
        self.dialog.theme.setCurrentText(str(settings_string["theme"]))
        self.dialog.lang.setCurrentText(str(settings_string["lang"]))

        result = self.dialog.exec()
        if result is not self.dialog.accepted:
            settings_string["ram"] = str(self.dialog.ram_select.currentText())
            settings_string["lang"] = str(self.dialog.lang.currentText())
            settings_string["theme"] = str(self.dialog.theme.currentText())

            with open('launch-settings.json', 'w', encoding='utf-8') as f:
                json.dump(settings_string,f,ensure_ascii=False, indent=4)

    def create_account(self):
        self.dialog = CreateAccountDialog(self)
        result = self.dialog.exec()
        if result is not self.dialog.accepted:
            data = {
                    str(self.dialog.account_name.text()):{
                        "vis_name":f"{str(self.dialog.account_name.text())} ({str(self.dialog.account_type.currentText())})",
                        "password":str(self.dialog.password.text()),
                        "type":str(self.dialog.account_type.currentText())
                    }
            }
            with open('accounts.json', 'w', encoding='utf-8') as f:
                json.dump(data,f, indent=4)

    def create_version(self):
        self.dialog = CreateAccountDialog(self)
        self.dialog.exec()

    def open_links(self):
        webbrowser.open_new_tab('https://t.me/NorthLauncher')

    def open_github(self):
        webbrowser.open_new_tab('https://github.com/PixelBoxGames/North-launcher')


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
