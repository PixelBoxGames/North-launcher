from PyQt6 import QtWidgets, uic
import sys, webbrowser, json, re, shutil
import minecraft_launcher_lib as mlib
from tkinter import messagebox
from PyQt6.QtGui import QPixmap
from pathlib import Path

base_path = Path.home() / ".nlauncher"
versions_path = base_path / "instances"

with open("launch-settings.json", "r") as f:
    selected_lang = json.load(f)

lang_path = f"resources/langs/{selected_lang["lang"]}.json"
with open(lang_path, "r") as f:
            current_lang = json.load(f)

def setup_launcher_directories():
    dirs = {base_path, versions_path}

    for directory in dirs:
        directory.mkdir(parents=True, exist_ok=True)
        print("Папка создана")

setup_launcher_directories()

def validate_input(text):
    pattern = r'^[a-zA-Z0-9_]+$'

    if re.match(pattern, text):
        return True
    else:
        return False

class InfoDialog(QtWidgets.QDialog):
    def __init__(self, parent = None):
        super().__init__(parent)
        uic.loadUi('info.ui', self)

        #localize

        with open('launch-settings.json', "r") as json_file:
            settings_string = json.load(json_file)

        lang_path = f"resources/langs/{settings_string["lang"]}.json"
        with open(lang_path, "r") as f:
            current_lang = json.load(f)
        self.abt_title.setText(str(current_lang['about']['abt_t']))
        self.abt_short_desc.setText(str(current_lang['about']['abt_sd']))
        self.abt_desc.setText(str(current_lang['about']['abt_d']))
        self.abt_link.setText(str(current_lang['about']['abt_l']))
        self.abt_follow.setText(str(current_lang['about']['abt_f']))


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

        self.ram = self.ram_select

        with open('launch-settings.json', "r") as json_file:
            settings_string = json.load(json_file)
        self.ram.setCurrentText(str(settings_string["ram"]))
        self.theme.setCurrentText(str(settings_string["theme"]))
        self.lang.setCurrentText(str(settings_string["lang"]))

        #локализаци
        lang_path = f"resources/langs/{settings_string["lang"]}.json"
        with open(lang_path, "r") as f:
            current_lang = json.load(f)
        self.ramtxt.setText(str(current_lang['settings']['ram']))
        self.title.setText(str(current_lang['settings']['title']))
        self.langtxt.setText(str(current_lang['settings']['lang']))
        self.pathtxt.setText(str(current_lang['settings']['path']))
        self.themetxt.setText(str(current_lang['settings']['theme']))
        self.mbtxt.setText(str(current_lang['settings']['mb']))


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
        self.del_account_btn.clicked.connect(self.delete_account)
        self.delete_btn.clicked.connect(self.del_inst)

        self.refresh_window()

    def refresh_window(self):
        self.account_select.clear()

        try:
            with open("accounts.json", "r", encoding = "utf-8") as f:
                data = json.load(f)

            for real_name, info in data.items():
                self.account_select.addItem(info["vis_name"], real_name)
        except FileNotFoundError:
            messagebox.showerror("Битые файлы", "У вас битые файлы accounts.json, пожалуйста, создайте аккаунт")

        with open("launch-settings.json", "r") as f:
                selected_lang = json.load(f)

        lang_path = f"resources/langs/{selected_lang["lang"]}.json"
        with open(lang_path, "r") as f:
            current_lang = json.load(f)

        # сборки
        inst_path = Path.home() / ".nlauncher" / "instances"

        if inst_path.exists():
            folders = [f.name for f in inst_path.iterdir() if f.is_dir()]

            self.version_select.clear()
            self.version_select.addItems(folders)



        # локализация
        self.play_btn.setText(str(current_lang['main']['play_btn']))
        self.info_btn.setText(str(current_lang['main']['about']))
        self.github_btn.setText(str(current_lang['main']['github']))
        self.links_btn.setText(str(current_lang['main']['links']))
        self.settings_btn.setText(str(current_lang['main']['settings_btn']))
        self.add_btn.setText(str(current_lang['main']['add']))
        self.wn_title.setText(str(current_lang['main']['wn_title']))
        self.short_desc.setText(str(current_lang['main']['wn_short_desc']))
        self.desc.setText(str(current_lang['main']['wn_desc']))
        self.links.setText(str(current_lang['main']['wn_follow']))

        with open("launch-settings.json", "r", encoding = "utf-8") as f:
                s_s = json.load(f)
        theme = s_s["theme"]

        if theme == "dark":
            pix = QPixmap("resources/textures/launcher/dark_bg.png")
        else:
            pix = QPixmap("resources/textures/launcher/light_bg.png")

        self.bg.setPixmap(pix)

    def open_info(self):
        self.dialog = InfoDialog(self)
        self.dialog.exec()

    def open_settings(self):
        self.dialog = SettingsDialog(self)
        self.ram = self.dialog.ram_select
        self.theme = self.dialog.theme
        self.lang = self.dialog.lang
        with open('launch-settings.json', "r") as json_file:
            settings_string = json.load(json_file)


        result = self.dialog.exec()
        if result:
            settings_string["ram"] = str(self.ram.currentText())
            settings_string["lang"] = str(self.lang.currentText())
            settings_string["theme"] = str(self.theme.currentText())

            with open('launch-settings.json', 'w', encoding='utf-8') as f:
                json.dump(settings_string,f,ensure_ascii=False, indent=4)



            self.refresh_window()

    def create_account(self):
        self.dialog = CreateAccountDialog(self)
        self.acname = self.dialog.account_name
        self.password = self.dialog.password

        with open('launch-settings.json', "r") as json_file:
            settings_string = json.load(json_file)

        lang_path = f"resources/langs/{settings_string["lang"]}.json"
        with open(lang_path, "r") as f:
            current_lang = json.load(f)

        result = self.dialog.exec()
        if result:
            if validate_input(str(self.acname.text())) and validate_input(str(self.password.text())):
                try:
                    with open("accounts.json", "r", encoding = "utf-8") as f:
                        data = json.load(f)

                except:
                    data = {}


                data[str(self.dialog.account_name.text())] = {
                        "vis_name":f"{str(self.acname.text())} ({str(self.dialog.account_type.currentText())})",
                        "password":str(self.dialog.password.text()),
                        "type":str(self.dialog.account_type.currentText())
                }
                with open('accounts.json', 'w', encoding='utf-8') as f:
                    json.dump(data,f, indent=4)
                self.refresh_window()
            else:
                messagebox.showerror(str(current_lang["sys"]["er_msg"]), str(current_lang["sys"]["er_cyr"]))

    def delete_account(self):
        target_rn = self.account_select.currentData()
        if not target_rn:
            messagebox.showerror(str(current_lang["sys"]["er_msg"]), str(current_lang["sys"]["er_mis"]))
            return

        try:
            with open("accounts.json", "r", encoding = "utf-8") as f:
                data = json.load(f)
        except Expection as e:
            messagebox.showerror(str(current_lang["sys"]["er_msg"]), str(current_lang["sys"]["er_js"]))

        if target_rn in data:
            del data[target_rn]

            with open("accounts.json", "w", encoding = "utf-8") as f:
                json.dump(data, f, indent = 4, ensure_ascii=False)

            self.refresh_window()
            messagebox.showinfo(str(current_lang["sys"]["suc_msg"]), f"{str(current_lang["sys"]["suc_del1"])}{str(target_rn)}{str(current_lang["sys"]["suc_del2"])}")

    def del_inst(self):
        inst_path = Path.home() / ".nlauncher" / "instances" / str(self.version_select.currentText())

        if inst_path.exists and inst_path.is_dir():
            shutil.rmtree(inst_path)
            messagebox.showinfo(str(current_lang["sys"]["suc_msg"]), f"{str(current_lang["sys"]["suc_del1"])}{str(self.version_select.currentText())}{str(current_lang["sys"]["suc_del2"])}")
            self.refresh_window()
        else:
            messagebox.showerror(str(current_lang["sys"]["er_msg"]), str(current_lang["sys"]["er_mis"]))


    def create_version(self):
        self.dialog = VerDialog(self)
        result = self.dialog.exec()
        if result:
            mod_sel = self.dialog.modloader_select
            ver_name = self.dialog.version_name
            ver_sel = self.dialog.version_select

            new_ver = versions_path / f"{str(ver_name.text())} ({str(mod_sel.currentText())} {str(ver_sel.currentText())})"
            ver_fold = new_ver / "versions"
            lib_fold = ver_fold / "libraries"
            as_fold = ver_fold / "assets"
            run_fold = ver_fold / "runtime"
            nat_fold = ver_fold / "natives"

            required_folders={ver_fold, lib_fold, as_fold, run_fold, nat_fold}

            for folder in required_folders:
                folder.mkdir(parents=True, exist_ok=True)

            self.refresh_window()

    def open_links(self):
        webbrowser.open_new_tab('https://t.me/NorthLauncher')

    def open_github(self):
        webbrowser.open_new_tab('https://github.com/PixelBoxGames/North-launcher')


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
