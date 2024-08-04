from PySide6.QtWidgets import QApplication, QFileDialog

app = QApplication([])

# Create a file dialog
file_dialog = QFileDialog()

# Set the file dialog to open in file selection mode
file_dialog.setFileMode(QFileDialog.ExistingFiles)

# Set the name filter to show only .txt files
file_dialog.setNameFilter("Application extension (*.dll)")

# Show the file dialog and get the selected file(s)
if file_dialog.exec_():
    selected_files = file_dialog.selectedFiles()
    print(selected_files)  # prints the list of selected files