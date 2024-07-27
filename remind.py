from PySide6.QtWidgets import QWidget,QPushButton, QHBoxLayout, QVBoxLayout, QApplication
from PySide6.QtWidgets import QListWidget, QAbstractItemView, QLabel, QLineEdit
import sys
import json
import os

DATA_FILE = "list_data.json"

#Main Window
class mainWindow(QWidget):
    def __init__(self,):
        super(mainWindow, self).__init__()

        self.setWindowTitle("Reminder App")
        self.setFixedSize(400,300)

        self.list_widget = QListWidget(self)
        self.list_widget.setSelectionMode(QAbstractItemView.MultiSelection)

        self.add_item_button = QPushButton("Add Item")
        self.add_item_button.clicked.connect(self.addItem)

        self.remove_item_button = QPushButton("Remove Item")
        self.remove_item_button.clicked.connect(self.removeSelectedItems)

        self.save_list_button = QPushButton("Save List")
        self.save_list_button.clicked.connect(self.saveList)

        self.load_list_button = QPushButton("Load List")
        self.load_list_button.clicked.connect(self.loadList)

        self.vertical_layout = QVBoxLayout()
        self.vertical_layout.addWidget(self.list_widget)
        self.vertical_layout.addWidget(self.add_item_button)
        self.vertical_layout.addWidget(self.remove_item_button)
        self.vertical_layout.addWidget(self.save_list_button)
        self.vertical_layout.addWidget(self.load_list_button)

        self.setLayout(self.vertical_layout)

        self.loadList()

    def addItem(self):
        self.w = addObjectWindow(self)
        self.w.show()

    def removeSelectedItems(self):
        for item in self.list_widget.selectedItems():
            row = self.list_widget.row(item)
            self.list_widget.takeItem(row)

    def addItemToList(self, item_text):
        self.list_widget.addItem(item_text)

    def saveList(self):
        items = []
        for index in range(self.list_widget.count()):
            item = self.list_widget.item(index)
            item_data = {
                'text': item.text()
            }
            items.append(item_data)

        with open(DATA_FILE, 'w') as f:
            json.dump(items, f)

    def loadList(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r') as f:
                items = json.load(f)

            self.list_widget.clear()
            for item_data in items:
                self.addItemToList(item_data['text'])

    def closeEvent(self, event):
        #Save the list data when the application is closed
        self.saveList()
        event.accept()



class addObjectWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__()

        self.parent_window = parent

        self.setWindowTitle("Add Item")
        self.setFixedSize(300,100)

        self.text_Label = QLabel("Title: ")
        self.line_edit_text = QLineEdit()

        self.horizontal_layout = QHBoxLayout()
        self.horizontal_layout.addWidget(self.text_Label)
        self.horizontal_layout.addWidget(self.line_edit_text)

        self.enter_button = QPushButton("Enter")
        self.enter_button.clicked.connect(self.addToList)
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.cancel)

        self.horizontal_layout_2 = QHBoxLayout()
        self.horizontal_layout_2.addWidget(self.enter_button)
        self.horizontal_layout_2.addWidget(self.cancel_button)

        self.vertical_layout = QVBoxLayout()
        self.vertical_layout.addLayout(self.horizontal_layout)
        self.vertical_layout.addLayout(self.horizontal_layout_2)

        self.setLayout(self.vertical_layout)
    
    def cancel(self):
        self.close()

    def addToList(self):
        remind_text = self.line_edit_text.text()
        if self.parent_window and remind_text:
            self.parent_window.addItemToList(remind_text)
            self.close()

    
#h

if __name__ == "__main__":   
    #Things to run mainWindow
    app = QApplication(sys.argv)
    w = mainWindow()
    w.show()
    app.exec()