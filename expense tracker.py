import sys
import sqlite3
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLineEdit, QMessageBox, QLabel
class Finance_app(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("YOU ARE BROKE MATE WHAT FINANCE LMAO")
        self.button = QPushButton("save expense", self)
        self.button.setObjectName("button")
        self.line = QLineEdit(self)
        self.line2 = QLineEdit(self)
        self.line.setPlaceholderText("Enter your expense amount in dollars")
        self.line2.setPlaceholderText("Enter Item Name")
        self.button.clicked.connect(self.save_item)
        self.button2 = QPushButton("show expense", self)
        self.button2.clicked.connect(self.show_expense)
        self.button2.setObjectName("button2")
        self.button3 = QPushButton("change expense price", self)
        self.button3.setObjectName("button3")
        self.button3.clicked.connect(self.change_expense)
        self.button4 = QPushButton("Delete expense", self)
        self.button4.clicked.connect(self.delete_expense)
        self.button4.setObjectName("button4")
        self.line3 = QLineEdit(self)
        self.line3.setPlaceholderText("Type ID to Delete Expense Or Change expense")
        self.label = QLabel("Save Your Expenses", self)
        self.database_sql()
        self.initUI()
    def initUI(self):
        self.setGeometry(430, 100, 550, 650)
        vbox = QVBoxLayout()
        vbox.addWidget(self.label)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        vbox.addStretch(1)
        vbox.addWidget(self.line2)
        vbox.addWidget(self.line)
        vbox.addWidget(self.line3)
        vbox.addWidget(self.button)
        vbox.addWidget(self.button2)
        vbox.addWidget(self.button3)
        vbox.addWidget(self.button4)
        self.setLayout(vbox)
        self.setStyleSheet("""
        QPushButton {color:Black;
        border-radius: 10px;
        border:1px solid black;
        font-size:30px;
        font-family:"Times New Roman";
        }     
        QPushButton#button:hover {background-color:lightgreen;}
        QPushButton#button2:hover {background-color:lightgreen;}
        QPushButton#button3:hover {background-color:lightgreen;}
        QPushButton#button4:hover {background-color:lightgreen;}
        QWidget {background-color:#44ebc7;}
        QLineEdit {color:Black;
        border:1px solid black;
        border-radius: 10px;
        font-size:20px;
        font-family:"Verdana";}
        QLabel {color:Black;
        font-size:20px;
        font-family:"Verdana";
        }
        """)

    def database_sql(self):
        self.conn = sqlite3.connect('finance.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS expenses(
                item_id integer PRIMARY KEY AUTOINCREMENT,
                item_name TEXT,
                amount DECIMAL,
                date DATETIME DEFAULT (datetime('now','localtime'))
                )""")
        self.conn.commit()
    def save_item(self):
        item = self.line2.text().lower()
        expense = self.line.text()
        if item and expense:
            self.cursor.execute("INSERT INTO expenses  (item_name,amount) values(?,?)", (item, expense))
            self.conn.commit()
            self.label.setText("Saved your expenses successfully")
            self.line2.clear()
            self.line.clear()
        else:
            self.label.setText("Enter your expenses information")

    def show_expense(self):
        self.cursor.execute("SELECT * FROM expenses")
        sql = self.cursor.fetchall()
        expense_list = []
        if sql:
            for item_id, item, expense, date in sql:
                expense_list.append(f"ID : {item_id}---{item} ${expense} : {date}")
            final_expense = "\n".join(expense_list)
            msg = QMessageBox()
            msg.setWindowTitle("fucking broke ass boi")
            msg.setText(final_expense)
            msg.setStyleSheet("""
                            background-color: #49fabb;
                            font-size: 20px;
                            font-family: 'Verdana';
                            color: black; 
                            border: 1px solid black;
                            border-radius: 10px;

                        """)
            msg.exec()
        else:
            no_data_msg = QMessageBox(self)
            no_data_msg.setWindowTitle("Expenses")
            no_data_msg.setText("Sorry, no expense available")
            no_data_msg.setStyleSheet("background-color: white; color: black; font-size: 20px;")
            no_data_msg.exec()

    def change_expense(self):
        text = self.line3.text().lower()
        text2 = self.line.text().lower()
        if text and text2:
            self.cursor.execute("UPDATE expenses SET amount = ? WHERE item_id = ?", (text2, text))
            self.label.setText("Changed your expenses successfully")
            self.conn.commit()
            self.line.clear()
            self.line3.clear()
        else:
            self.label.setText("Enter your expenses information")
    def delete_expense(self):
        text = self.line3.text().strip()
        if text:
            self.cursor.execute("delete from expenses where item_id = ?", (text,))
            if self.cursor.rowcount > 0:
                self.conn.commit()
                self.label.setText("Deleted your expense successfully")
                self.line3.clear()
        else:
            self.label.setText("Please enter correct ID")
    def closeEvent(self, event):
        self.conn.close()
        event.accept()
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Finance_app()
    window.show()
    sys.exit(app.exec())
