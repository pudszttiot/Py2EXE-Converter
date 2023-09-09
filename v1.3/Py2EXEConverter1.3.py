import sys
import os
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QLabel,
    QVBoxLayout,
    QWidget,
    QCheckBox,
    QFileDialog,
    QLineEdit,
    QMessageBox,
)
from PyQt5.QtGui import QIcon, QPixmap
import subprocess
from PyQt5.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Py2EXE")
        self.setWindowIcon(QIcon("new.ico"))
        self.setFixedSize(220, 500)  # Increased window size

        layout = QVBoxLayout()

        # Add image label
        image_label = QLabel()
        image_path = "C:/Users/pudszTTIOT/Desktop/py/Python Creations/Completed/Projects/Py2EXE Converter/Images/py-icon-7.png"
        pixmap = QPixmap(image_path)
        pixmap = pixmap.scaledToWidth(150)
        image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignCenter)
        image_label.setToolTip("PY2EXE...TTIOT")
        layout.addWidget(image_label)

        self.label_2 = QLabel(self)
        self.setGeometry(0, 0, 200, 480)
        self.label_2.resize(500, 500)
        self.label_2.setStyleSheet("background-image : url(image.png)")

        self.show()
        self.setFixedSize(self.size())

        label = QLabel("Select Python files to convert:")
        layout.addWidget(label)

        self.button = QPushButton("Browse for Python files")
        self.button.clicked.connect(self.browse_python_files)
        self.button.setToolTip("Click to select your program (pythonscript.py)")
        layout.addWidget(self.button)

        self.icon_label = QLabel("Select an Icon: (Optional)")
        layout.addWidget(self.icon_label)

        self.icon_button = QPushButton("Browse for Icon")
        self.icon_button.clicked.connect(self.browse_icon_file)
        self.icon_button.setToolTip("Click to select a custom icon for the application")
        layout.addWidget(self.icon_button)

        self.name_label = QLabel("Enter application name:")
        layout.addWidget(self.name_label)

        self.name_input = QLineEdit()
        self.name_input.setToolTip("Enter the desired application name")
        layout.addWidget(self.name_input)

        self.output_label = QLabel("Select an output folder:")
        layout.addWidget(self.output_label)

        self.output_button = QPushButton("Browse for Output Folder")
        self.output_button.clicked.connect(self.browse_output_folder)
        self.output_button.setToolTip("Click to choose where to save the application")
        layout.addWidget(self.output_button)

        self.options = {
            "--onefile": "Create a single executable file",
            "--console": "Open a console window for the application",
            "--noconsole": "Do not open a console window for the application",
        }

        self.checkboxes = []
        for option in self.options:
            checkbox = QCheckBox(option)
            checkbox.setToolTip(self.options[option])
            layout.addWidget(checkbox)
            self.checkboxes.append(checkbox)

        self.convert_button = QPushButton("Convert")
        self.convert_button.clicked.connect(self.convert_to_exe)
        self.convert_button.setToolTip("Click to convert the Python file(s) to EXE")
        layout.addWidget(self.convert_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def browse_python_files(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Select Python files", "", "Python Files (*.py)")
        if files:
            self.python_files = files
            self.button.setText("Python files selected")

    def browse_icon_file(self):
        icon_path, _ = QFileDialog.getOpenFileName(
            self, "Select an Icon file", "", "Icon Files (*.ico)"
        )
        if icon_path:
            self.icon_file_path = icon_path
            self.icon_button.setText("Icon file selected")

    def browse_output_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select output folder")
        if folder_path:
            self.output_folder_path = folder_path
            self.output_button.setText("Output folder selected")

    def convert_to_exe(self):
        if hasattr(self, "python_files"):
            selected_options = [
                option
                for option, checkbox in zip(self.options, self.checkboxes)
                if checkbox.isChecked()
            ]
            
            pyinstaller_command = [
                "pyinstaller",
                "--onefile",  # To create a single .exe file
                *selected_options,
                *self.python_files,  # Add all selected .py files
            ]

            if hasattr(self, "icon_file_path"):
                pyinstaller_command.insert(1, f"--icon={self.icon_file_path}")
            if hasattr(self, "output_folder_path"):
                build_folder_path = os.path.join(self.output_folder_path, "build")
                pyinstaller_command.extend(
                    [
                        "--distpath",
                        self.output_folder_path,
                        "--workpath",
                        build_folder_path,
                    ]
                )
                spec_file_path = os.path.join(self.output_folder_path, "output.spec")
                pyinstaller_command.extend(
                    ["--specpath", self.output_folder_path, "--name", spec_file_path]
                )
            app_name = self.name_input.text()
            if app_name:
                pyinstaller_command.append(f"--name={app_name}")

            result = subprocess.call(pyinstaller_command)

            if result == 0:
                QMessageBox.information(
                    self, "Conversion Complete", "Conversion to EXE was successful!"
                )
            else:
                QMessageBox.critical(
                    self, "Conversion Failed", "Conversion to EXE failed!"
                )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
