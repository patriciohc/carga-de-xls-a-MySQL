#!/usr/bin/python
#encoding:utf-8
import logging
from xlrd import open_workbook
from xml.dom.minidom import parse
import xml.dom.minidom
import sys
from Choose_file import Ui_MainWindow
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from DataBase import DB
from Modelos import *


# variables que definen la posicion de las celdas donde se encuentran
# la informacion en el archivo xls
C = 1  # columnas
R = 0  # filas
PARA = (0,2)
LABORATORISTA = (0,3)
FOLIO = (7,4)
FECHA = (7,6)
CLIENTE = (0,9)
DESCRIPCION_REPORTE = (0,10)
CABECERA = 12 # FILA 13
DESCRIPCION_MUESTRA = 0 # COLUMNA 1
NO_COLADA = 1 # COLUMNA 1 FILA DESPUES DE CABECERA
NO_MUESTRA = 2 # COLUMNA 2 "
NO_ANALISIS = 3 # COLUMNA
ANALISIS = 4 # EMPIEZAN APARTIR DE COLUMNA 5
OBSERVACIONES = 0 #columna = 1, fila = ultimo analisis + tres filas

logging.basicConfig(filename='./loginfo.log', level=logging.INFO)

MSG_NO_FILE = """"
No ha seleccionado ningun archivo!
De clic en el boton choose y vuelva a intentarlo.
"""
MSG_DONE = """
El archivo se cargado correctamente, consulte el
archivo info.log para mas detalles.
"""

class Xls_to_db(QMainWindow, Ui_MainWindow):
    def __init__(self):
        QDialog.__init__(self)
        self.setupUi(self)
        self.btChooseFile.clicked.connect(self.show_dialog)
        self.btLoadFile.clicked.connect(self.load_file)
        self.btClose.clicked.connect(exit)

    def show_dialog(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', './')
        self.txtFile.setText(fname)

    def load_file(self):
        fname = self.txtFile.text()
        try:
            self.xls = open_workbook(fname)
        except IOError:
            self.msg_info(MSG_NO_FILE)
            return 0
        self.db = DB()
        self.process_book()
        self.msg_info(MSG_DONE)

    def msg_info(self,msg):
        # QMessageBox.information (QWidget parent, QString caption, QString text,
        # int button0, int button1 = 0, int button2 = 0)
        QMessageBox.information(self, "Informacion", msg, QMessageBox.Ok)


    def process_book(self):
        for sheet_index in range(self.xls.nsheets):
            sheet = self.xls.sheet_by_index(sheet_index)
            self.process_sheet(sheet)

    def process_sheet(self,sheet):
        sheet_name = sheet.name
        print "procesando: " + sheet_name
        if sheet.ncols < 8 or sheet.nrows < 14:  # no cumple con el tamaño adecuado
            logging.info("sheet %s: no se hace nada numero de columnas o filas no cumple" % (sheet_name))
            return 0
        folio = sheet.cell( FOLIO[C], FOLIO[R]).value
        if (folio == "" or folio == None):  # comprueba que exista numero de folio
            print "no se hace nada para: " + sheet_name  
            return 0
        try:
# separa la cadena 'Folio:xxxxx' para obtener unicamente numero de folio
            folio = folio.split(':')[1]
            folio = folio.strip() #  elimina espacios
        except IndexError:
            logging.info("sheet %s: formato de folio incorrecto" % (sheet_name))
            return 0
        cliente = sheet.cell(CLIENTE[C],CLIENTE[R]).value
        try:
            cliente = cliente.split(':')[1]
            cliente = cliente.strip()
        except IndexError:
            logging.info("sheet %s: formato de cliente incorrecto" % (sheet_name))
            return 0

        if (cliente.upper() == "INTERNO" or cliente == ""): # interno no se procesa
            return 0 
        fecha = sheet.cell(FECHA[C],FECHA[R]).value
        try:
            fecha = fecha.split(':')[1].strip()
            fecha = fecha.strip()
        except IndexError:
            logging.info("sheet %s: formato de fecha incorrecto" %(sheet_name))
            return 0;
        para = sheet.cell(PARA[C],PARA[R]).value
        try:
            para = para.split(':')[1].strip()
            para = para .strip()
        except IndexError:
            logging.info("sheet %s: formato de destinatario incorrecto" %(sheet_name))
            return 0

        lab = sheet.cell(LABORATORISTA[C],LABORATORISTA[R]).value  #laboratorista
        des_reporte = sheet.cell(DESCRIPCION_REPORTE[C],DESCRIPCION_REPORTE[R]).value  # descripcion reporte
        reporte = Reporte(folio,para, lab, fecha, cliente, des_reporte)
        reporte.save(self.db)
        vacio = 0 # filas vacias encontradas si es mayor a tres los analisis han terminado
        fila_actual = CABECERA + 1 # inicio de analisis
# recorre la tabla de analisis y los guarda en la base de datos
        while vacio < 3 and fila_actual < sheet.nrows:
            no_analisis = sheet.cell(fila_actual,NO_ANALISIS).value
            if no_analisis == "":
                vacio += 1
                continue
            try:
                no_analisis = int(no_analisis)
            except ValueError:
                logging.info("sheet %s: numero de analisis debe ser entero fila %d" 
                                %(sheet_name, fila_actual))
                fila_actual += 1
                continue
            des_muestra = sheet.cell(fila_actual, DESCRIPCION_MUESTRA).value
            des_muestra = des_muestra.replace("'"," ")
            no_colada = sheet.cell(fila_actual, NO_COLADA).value
            no_muestra = sheet.cell(fila_actual, NO_MUESTRA).value
            registro = Registro(no_analisis)
            registro.save(self.db)
            muestra = Escoria(no_analisis, folio, no_colada, des_muestra)
            muestra.save(self.db)
            analisis = self.process_table(sheet,fila_actual)
            analisis_escoria = AnalisisEscoria(no_analisis,analisis)
            analisis_escoria.save(self.db)
            fila_actual+=1

        obs = ""
        if fila_actual < sheet.nrows:
            obs = sheet.cell(fila_actual, OBSERVACIONES).value
        if obs == "" and fila_actual < sheet.nrows:
            obs = sheet.cell(fila_actual+1, OBSERVACIONES).value
        if not (obs == ""):
            reporte.add_observaciones(self.db, obs)


    def process_table(self, sheet, fila_actual):
        elemento = 0
        c_vacio = 0
        analisis = []
        while not c_vacio and ANALISIS+elemento < sheet.ncols:
            parametro = sheet.cell(CABECERA,ANALISIS+elemento).value
            parametro = parametro.strip()
            #print  sheet.cell(CABECERA,ANALISIS+el).
            if parametro == "":
                c_vacio = 1
            else:
                value = sheet.cell(fila_actual, ANALISIS+elemento).value
                try:
                    value = float(value)
                    #analisis += [(parametro,val)]
                    dato = {
                        'parametro': parametro.replace(" ","_"), 
                        'value': value,
                    }
                    analisis += [dato]
                except ValueError:
                    pass
                elemento += 1
        return analisis

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.processEvents()
    convert = Xls_to_db()
    convert.show()
    sys.exit(app.exec_())


