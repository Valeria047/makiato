import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QMessageBox


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('077.ui', self)
        self.con = sqlite3.connect("coffee.db")
        self.pushButton.clicked.connect(self.add_film)
        self.pushButton_2.clicked.connect(self.edit_film)
        self.dialogs = []
        self.select_data()
        #self.tableWidget.currentChanged.connect(self.cell_table)

    def add_film(self):
        dialog = AddFilm(self)
        dialog.show()

    def select_data(self):
        query = "SELECT * FROM coffee"
        res = self.con.cursor().execute(query)
        print(res)
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setHorizontalHeaderLabels(["ID", "Название", 'степень обжарки', 'молотый/в зернах', 'описание вкуса',
                                                    'цена', 'объем упаковки'])
        for i, row in enumerate(res):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))


    def edit_film(self):
        rows = list(set([i.row() for i in self.tableWidget.selectedItems()]))
        ids = [self.tableWidget.item(i, 0).text() for i in rows]
        if not ids:
            self.statusBar().showMessage('Ничего не выбрано')
            return
        else:
            self.statusBar().showMessage('')
        print(ids)
        dialog = AddFilm(self, film_id=ids[0])
        dialog.show()


class AddFilm(QMainWindow):
    def __init__(self, parent=None, film_id=None):
        super().__init__(parent)
        self.con = sqlite3.connect("coffee.db")
        self.d = {}
        uic.loadUi('addfilm.ui', self)
        self.pushButton.clicked.connect(self.add_elem)

    def get_elem(self):
        cur = self.con.cursor()
        res = cur.execute("""SELECT * from coffee""".format(self.film_id)).fetchone()
        self.title.setPlainText(res[1])
        self.year.setPlainText(str(res[2]))
        self.year_2.setCurrentText(res[3])
        self.year_5.setPlainText(str(res[4]))
        self.year_3.setPlainText(str(res[4]))
        self.year_4.setPlainText(str(res[4]))

    def add_elem(self):
        cur = self.con.cursor()
        try:
            id_off = cur.execute("SELECT max(id) FROM coffee").fetchone()[0]
            new_data = (id_off + 1, self.title.toPlainText(), self.year.toPlainText(),
                        self.year_2.toPlainText(), self.year_5.toPlainText(), int(self.year_4.toPlainText()),
                        int(self.year_3.toPlainText()))
            print(new_data)
            cur.execute("INSERT INTO coffee VALUES (?,?,?,?,?,?,?)", new_data)
        except ValueError:
            self.statusBar().showMessage("Неверно заполнена форма")
        else:
            print(1)
            self.con.commit()
            print(1)
            self.parent().select_data()
            print(1)
            self.close()

    def edit_elem(self):
        cur = self.con.cursor()
        try:
            new_data = (self.film_id, self.title.toPlainText(), self.year.toPlainText(),
                        self.year_2.toPlainText(), self.year_5.toPlainText(), int(self.year_4.toPlainText()), int(self.year_3.toPlainText()))
            cur.execute("UPDATE coffee SET (?,?,?,?,?,?,?)", new_data)
        except ValueError:
            self.statusBar().showMessage("Неверно заполнена форма")
        else:
            self.con.commit()
            self.parent().select_data()
            self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = MyWidget()
    form.show()
    sys.exit(app.exec())