import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QCheckBox, QFileDialog, QLineEdit, QMessageBox
from PyQt5.QtGui import QIcon
import subprocess


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Py2EXE Converter")
        # Replace "icon.png" with the path to your desired icon file
        self.setWindowIcon(QIcon(
            "G:/Software/py/Python Creations/Completed/Projects/Py2EXE Converter/Py2EXE.ico"))

        layout = QVBoxLayout()

        label = QLabel("Select a Python file to convert:")
        layout.addWidget(label)
        self.button = QPushButton("Browse for Python file")
        self.button.clicked.connect(self.browse_python_file)
        layout.addWidget(self.button)

        self.icon_label = QLabel("Select an Icon: (Optional)")
        layout.addWidget(self.icon_label)

        self.icon_button = QPushButton("Browse for Icon")
        self.icon_button.clicked.connect(self.browse_icon_file)
        layout.addWidget(self.icon_button)

        self.name_label = QLabel("Enter application name:")
        layout.addWidget(self.name_label)

        self.name_input = QLineEdit()
        layout.addWidget(self.name_input)

        self.output_label = QLabel("Select an output folder:")
        layout.addWidget(self.output_label)

        self.output_button = QPushButton("Browse for Output Folder")
        self.output_button.clicked.connect(self.browse_output_folder)
        layout.addWidget(self.output_button)

        self.options = [
            "--onefile",
            "--windowed",
            "--noconsole"
        ]

        self.checkboxes = []
        for option in self.options:
            checkbox = QCheckBox(option)
            layout.addWidget(checkbox)
            self.checkboxes.append(checkbox)

        self.convert_button = QPushButton("Convert")
        self.convert_button.clicked.connect(self.convert_to_exe)
        layout.addWidget(self.convert_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def browse_python_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select a Python file")
        if file_path:
            self.python_file_path = file_path

    def browse_icon_file(self):
        icon_path, _ = QFileDialog.getOpenFileName(
            self, "Select an Icon file", "", "Icon Files (*.ico)")
        if icon_path:
            self.icon_file_path = icon_path

    def browse_output_folder(self):
        if folder_path := QFileDialog.getExistingDirectory(
            self, "Select output folder"
        ):
            self.output_folder_path = folder_path

    def convert_to_exe(self):
        if not hasattr(self, 'python_file_path'):
            return
        selected_options = [option for option, checkbox in zip(
            self.options, self.checkboxes) if checkbox.isChecked()]
        pyinstaller_command = ["pyinstaller"] + \
                selected_options + [self.python_file_path]

        if hasattr(self, 'icon_file_path'):
            pyinstaller_command.insert(1, f"--icon={self.icon_file_path}")

        if hasattr(self, 'output_folder_path'):
            build_folder_path = os.path.join(
                self.output_folder_path, "build")
            pyinstaller_command.extend(
                ["--distpath", self.output_folder_path, "--workpath", build_folder_path])
            spec_file_path = os.path.join(
                self.output_folder_path, "output.spec")
            pyinstaller_command.extend(
                ["--specpath", self.output_folder_path, "--name", spec_file_path])

        if app_name := self.name_input.text():
            pyinstaller_command.append(f"--name={app_name}")

        result = subprocess.call(pyinstaller_command)

        if result == 0:
            QMessageBox.information(
                self, "Conversion Complete", "Conversion to EXE was successful!")
        else:
            QMessageBox.critical(
                self, "Conversion Failed", "Conversion to EXE failed!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())