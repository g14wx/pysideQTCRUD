from pymysql.connections import Connection as connectionPymysql
from Models.Product import Product
from PySide6.QtWidgets import QWidget, QPushButton, QTableWidget, QTableWidgetItem, QLineEdit, QLabel
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
import sys
import os
import pathlib


class ProductsController:
    def __init__(self, conn: connectionPymysql, ui_login=QWidget):
        self.ui_login = ui_login
        self.conn = conn
        self.productModel = Product(conn=self.conn)

    def show_principal(self):
        # ----------- Cargando la vista principal -----------------------#
        loader = QUiLoader()
        path = os.path.join(pathlib.Path().absolute(), "views/principal.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        self.ui = loader.load(ui_file)
        ui_file.close()
        self.ui.show()
        self.setWidgets()
        self.setTableWithItems()

    def setWidgets(self):
        self.btnCreate: QPushButton = self.ui.btnCreate
        self.btnList: QPushButton = self.ui.btnList
        self.table: QTableWidget = self.ui.productsTable
        self.btnLogout: QPushButton = self.ui.btnLogout
        self.btnList.clicked.connect(self.list_products)
        self.btnCreate.clicked.connect(self.showCreateForm)
        self.btnLogout.clicked.connect(self.back_login)
        self.table.itemClicked.connect(self.show_product)

    def back_login(self):
        self.ui_login.show()
        self.ui.close()

    def list_products(self):
        products = self.productModel.get_products()
        self.table.setRowCount(0)
        self.setTableWithItems()

    def setTableWithItems(self):
        self.table.setRowCount(0)
        products = self.productModel.get_products()
        for row_number, row_data in enumerate(products):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def showCreateForm(self):
        loader = QUiLoader()
        path = os.path.join(pathlib.Path().absolute(), "views/productForm.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        self.ui_form = loader.load(ui_file)
        ui_file.close()
        self.ui_form.show()
        self.SetFormWidgets()

    def SetFormWidgets(self):
        self.btnSave: QPushButton = self.ui_form.btnSave
        self.lineCode: QLineEdit = self.ui_form.lineCode
        self.lineTitle: QLineEdit = self.ui_form.lineTitle
        self.linePrice: QLineEdit = self.ui_form.linePrice
        self.lineCat: QLineEdit = self.ui_form.lineCat
        self.lblEdit: QLabel = self.ui_form.lblEdit
        self.btnSave.clicked.connect(self.save_event)

    def save_event(self):
        if self.lblEdit.text() != "editing":
            self.productModel.save(cod=self.lineCode.text(), title=self.lineTitle.text(), price=self.linePrice.text(),
                                   cat=self.lineCat.text())
            print("saved!")

        else:
            self.productModel.update(cod=self.lineCode.text(), title=self.lineTitle.text(), price=self.linePrice.text(),
                                     cat=self.lineCat.text())
        self.setTableWithItems()
        self.ui_form.close()

    def show_product(self):
        print("show_product selected")
        if self.table.currentRow() is not None:
            row = self.table.currentRow()
            print(row)
            cod = self.table.item(row, 0).text()
            print(cod)
            product = self.productModel.get_product(cod=cod)
            if product is not None:
                print(product)
                loader = QUiLoader()
                path = os.path.join(pathlib.Path().absolute(), "views/dialog_product.ui")
                ui_dialog_file = QFile(path)
                ui_dialog_file.open(QFile.ReadOnly)
                self.ui_dialog = loader.load(ui_dialog_file)
                self.ui_dialog.show()
                self.setWidgetsDialog(product)
        else:
            print("error cant find a clicked column")

    def setWidgetsDialog(self, product):
        lineCode: QLabel = self.ui_dialog.lineCode
        lineTitle: QLabel = self.ui_dialog.lineTitle
        linePrice: QLabel = self.ui_dialog.linePrice
        lineCat: QLabel = self.ui_dialog.lineCat
        btnOk: QPushButton = self.ui_dialog.btnOk
        btnEdit: QPushButton = self.ui_dialog.btnEdit
        btnDelete: QPushButton = self.ui_dialog.btnDelete
        btnDelete.clicked.connect(self.delete_product)
        btnOk.clicked.connect(self.close_dialog)
        btnEdit.clicked.connect(self.edit_this_product)
        self.productForEdit = product
        lineCode.setText(product[0])
        lineTitle.setText(product[1])
        linePrice.setText(product[2])
        lineCat.setText(product[3])

    def close_dialog(self):
        self.ui_dialog.close()

    def edit_this_product(self):
        self.showCreateForm()
        self.lblEdit.setText("editing")
        self.ui_dialog.close()
        self.lineCat.setText(self.productForEdit[3])
        self.lineCode.setText(self.productForEdit[0])
        self.lineCode.setReadOnly(1)
        self.lineTitle.setText(self.productForEdit[1])
        self.linePrice.setText(self.productForEdit[2])

    def delete_product(self):
        self.productModel.delete(self.productForEdit[0])
        self.setTableWithItems()
        self.ui_dialog.close()

