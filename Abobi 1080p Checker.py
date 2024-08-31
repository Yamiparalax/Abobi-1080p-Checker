import sys
import os
import subprocess
import json
from pathlib import Path
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox

CONFIG_FILE = "last_config.json"

class Worker(QtCore.QThread):
    update_progress = QtCore.pyqtSignal(str)
    finished_signal = QtCore.pyqtSignal()

    def __init__(self, video_files):
        super().__init__()
        self.video_files = video_files

    def run(self):
        for input_file in self.video_files:
            self.delete_if_not_1080p(input_file)
        self.finished_signal.emit()

    def delete_if_not_1080p(self, input_file):
        try:
            # Get video resolution using ffprobe
            result = subprocess.run(
                [
                    'ffprobe',
                    '-v', 'error',
                    '-select_streams', 'v:0',
                    '-show_entries', 'stream=width,height',
                    '-of', 'csv=p=0',
                    str(input_file)
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            if result.returncode == 0:
                output = result.stdout.decode().strip()
                width, height = map(int, output.split(','))

                if width < 1920 or height < 1080:
                    os.remove(input_file)
                    self.update_progress.emit(f"Deleted: {Path(input_file).name}")
                else:
                    self.update_progress.emit(f"Retained: {Path(input_file).name}")
            else:
                error_message = result.stderr.decode()
                self.update_progress.emit(f"Error processing {input_file}: {error_message}")

        except Exception as e:
            self.update_progress.emit(f"Unexpected error: {e}")

class Ui_MainWindow(QtCore.QObject):
    log_signal = QtCore.pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.video_files = []
        self.is_processing = False
        self.config = self.load_config()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(600, 400)
        MainWindow.setStyleSheet("background-color: #24273a; color: #fff;")

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(170, 0, 261, 61))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label.setFont(font)
        self.label.setObjectName("label")

        self.lineEdit_inputFolder = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_inputFolder.setGeometry(QtCore.QRect(10, 70, 280, 38))
        self.lineEdit_inputFolder.setPlaceholderText("Enter input folder path here")
        self.lineEdit_inputFolder.setObjectName("lineEdit_inputFolder")

        self.pushButton_process = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_process.setGeometry(QtCore.QRect(300, 70, 280, 38))
        self.pushButton_process.setObjectName("pushButton_process")

        self.textEdit_log = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_log.setGeometry(QtCore.QRect(10, 120, 580, 260))
        self.textEdit_log.setStyleSheet("background-color: #181926; color: #fff;")
        self.textEdit_log.setObjectName("textEdit_log")

        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.pushButton_process.clicked.connect(self.process_videos)
        self.log_signal.connect(self.update_log)

        # Load the saved configuration into the interface
        self.load_config_to_interface()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Video Quality Checker"))
        self.label.setText(_translate("MainWindow", "Video Quality Checker"))
        self.pushButton_process.setText(_translate("MainWindow", "Check and Delete Videos"))

    @QtCore.pyqtSlot(str)
    def update_log(self, message):
        self.textEdit_log.append(message)
        self.textEdit_log.verticalScrollBar().setValue(self.textEdit_log.verticalScrollBar().maximum())

    def log(self, message):
        self.log_signal.emit(message)

    def process_videos(self):
        if self.is_processing:
            self.show_error("Already processing videos.")
            return

        self.video_files = []
        input_path = Path(self.lineEdit_inputFolder.text().strip())

        if not input_path.exists() or not input_path.is_dir():
            self.show_error("The provided input folder path does not exist or is not a directory.")
            return

        for file_path in input_path.rglob('*'):
            if file_path.suffix.lower() in ['.mp4', '.mkv', '.avi', '.webm', '.mov']:
                self.video_files.append(str(file_path))

        if not self.video_files:
            self.show_error("No video files found in the input folder.")
            return

        self.is_processing = True
        self.log("Starting video processing...")

        self.worker = Worker(self.video_files)
        self.worker.update_progress.connect(self.log)
        self.worker.finished_signal.connect(self.on_processing_finished)
        self.worker.start()

    def show_error(self, message):
        QMessageBox.critical(None, "Error", message, QMessageBox.Ok)

    def on_processing_finished(self):
        self.is_processing = False
        self.log("Processing completed.")

    def save_config(self, output_folder):
        new_config = {
            "output_folder": output_folder
        }

        # Save the latest configuration only
        with open(CONFIG_FILE, 'w') as f:
            json.dump(new_config, f, indent=4)

    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        return {}

    def load_config_to_interface(self):
        config = self.load_config()
        if config:
            self.lineEdit_inputFolder.setText(config.get("output_folder", ""))

def main():
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
