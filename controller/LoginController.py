from Models.User import User
from database.connection import connection
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
from PySide6.QtWidgets import QWidget
from controller.ProductsController import ProductsController
import os
import pathlib

class LoginController:
    def __init__(self, conn: connection):
        self.conn = conn
        self.user = User(conn=conn)

    def log_in(self,username:str,password:str,loginUi):
        if username and password:
            print("login pressed!")
            user = self.user.get_user(username,password)
            if user:
                print("login succesfull")
                self.showPrincipal(loginUi=loginUi)
            else:
                print("not login")

    def showPrincipal(self,loginUi : QWidget):
        # cerrramos la instancia de la ventana de login anterior
        # esta es necesaria que sea una instancia self que se envie en el metodo de log_in de esta clase
        loginUi.hide()
        # instanciamos el controlador, para que asi podamos llamar a la funcion show_principal, quien se encargara de
        # cargar la .ui correspondiente
        self.principalController = ProductsController(conn=self.conn,ui_login=loginUi)
        self.principalController.show_principal()



