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
        self.setWindowTitle("Py2EXE Converter")
        # Replace "icon.png" with the path to your desired icon file
        self.setWindowIcon(
            QIcon(
                "new.ico"
            )
        )

        layout = QVBoxLayout()

        # Add image label
        image_label = QLabel()
        image_path = "G:\Software\py\Python Creations\Completed\Projects\Py2EXE Converter\Images\py-icon-7.png"  # Replace with the path to your image
        pixmap = QPixmap(image_path)
        pixmap = pixmap.scaledToWidth(150)  # Adjust the width as needed
        image_label.setPixmap(pixmap)
        image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignCenter)
        image_label.setToolTip("PY2EXE...TTIOT")
        layout.addWidget(image_label)


        # creating a label widget
        self.label_2 = QLabel(self)

        # setting  the geometry of window
        self.setGeometry(0, 0, 200, 480)

        # resizing the widget
        self.label_2.resize(500, 500)
        
  
        # setting up the border and adding image to background
        self.label_2.setStyleSheet("background-image : url(image.png)")
 

        # show all the widgets
        self.show()

        # Lock the window size
        self.setFixedSize(self.size())
  
  

        label = QLabel("Select a Python file to convert:")
        label.setToolTip("")
        layout.addWidget(label)
        self.button = QPushButton("Browse for Python file")
        self.button.clicked.connect(self.browse_python_file)
        self.button.setToolTip("Click to select your program (pythonscript.py)")
        layout.addWidget(self.button)

        self.icon_label = QLabel("Select an Icon: (Optional)")
        self.icon_label.setToolTip("")
        layout.addWidget(self.icon_label)

        self.icon_button = QPushButton("Browse for Icon")
        self.icon_button.clicked.connect(self.browse_icon_file)
        self.icon_button.setToolTip("Click to select a custom icon for the application")
        layout.addWidget(self.icon_button)

        self.name_label = QLabel("Enter application name:")
        self.name_label.setToolTip("")
        layout.addWidget(self.name_label)

        self.name_input = QLineEdit()
        self.name_input.setToolTip("Enter the desired application name")
        layout.addWidget(self.name_input)

        self.output_label = QLabel("Select an output folder:")
        self.output_label.setToolTip("")
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
        self.convert_button.setToolTip("Click to convert the Python file to EXE")
        layout.addWidget(self.convert_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def browse_python_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select a Python file")
        if file_path:
            self.python_file_path = file_path
            self.button.setText("Python file selected")

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
        if hasattr(self, "python_file_path"):
            selected_options = [
                option
                for option, checkbox in zip(self.options, self.checkboxes)
                if checkbox.isChecked()
            ]
            pyinstaller_command = (
                ["pyinstaller"] + selected_options + [self.python_file_path]
            )

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
