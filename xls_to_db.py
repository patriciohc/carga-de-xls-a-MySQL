#encoding:utf-8
import logging
from xlrd import open_workbook
from xml.dom.minidom import parse
import xml.dom.minidom
import sys
import MySQLdb
from Choose_file import Ui_MainWindow
from PyQt4.QtGui import *
from PyQt4.QtCore import *

DB_HOST = 'localhost' 
DB_USER = 'root' 
DB_PASS = 'root' 
DB_NAME = 'laboratorio' 

# variables que definen la posicion de las celdas donde se encuentran
# la informacion en el archivo xlsC = 1 # columnas 
R = 0 # filas
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


class DB():
    def __init__(self):
        datos = [DB_HOST, DB_USER, DB_PASS, DB_NAME] 
        self.conn = MySQLdb.connect(*datos)  # Conectar a la base de datos 

    def run_query(self,query):
        logging.info(query)
        cursor = self.conn.cursor()  # Crear un cursor 
        try:
            cursor.execute(query)  # Ejecutar una consulta  
            if query.upper().startswith('SELECT'): 
                data = cursor.fetchall()  # Traer los resultados de un select 
            else:
                self.conn.commit()
                data = None
        except MySQLdb.Error as err:
            logging.error("error msyql ")
            data = None
        cursor.close()  # Cerrar el cursor
        return data

    def close(self): 
        self.conn.close()  # Cerrar la conexión 
 

    
class Reporte():
    def __init__(self,folio,para="",laboratorista="",fecha = "", cliente="",
                descripcion="",observaciones=""):
        try:
            folio = int(folio)
        except ValueError:
            pass
        self.folio = str(folio)
        self.para = para
        self.laboratorista = laboratorista
        self.fecha = fecha
        self.cliente = cliente
        self.descripcion = descripcion
        self.observaciones = observaciones


    def save(self, conexion):
        query = """
                insert into principal_reporte(folio,para,laboratorista, fecha, 
                cliente, descripcion, observaciones) values('%s', '%s', '%s',
                '%s', '%s','%s','%s')""" % (self.folio, self.para, 
                self.laboratorista, self.fecha, self.cliente, self.descripcion, 
                self.observaciones)
        conexion.run_query(query)

    def add_observaciones(self,conexion):
        query = """ UPDATE principla_reporte SET observaciones='%s' 
            WHERE folio='%s' """ % (self.observaicones, self.folio) 
        conexion.run_query(query)


class Muestra():
    def __init__(self,no_analisis,folio_reporte,no_colada,no_muestra,
                descripcion,image=0):
        self.no_analisis = int(no_analisis)
        try:
            folio_reporte = int(folio_reporte)
            no_colada = int(no_colada)
            no_muestra = int(no_muestra)
        except ValueError:
            pass
        self.folio_reporte = str(folio_reporte)
        self.no_colada = str(no_colada)
        self.no_muestra = str(no_muestra)
        self.descripcion = descripcion
        self.image = image

    def save(self,conexion):
        query = """ insert into principal_muestra(no_analisis, folio_reporte_id,
                    no_colada, no_muestra, descripcion, imagen_id) values(%s, 
                    '%s', '%s', '%s', '%s', %d)""" % (self.no_analisis, 
                    self.folio_reporte, self.no_colada, self.no_muestra, 
                    self.descripcion, self.image )
        conexion.run_query(query)


class Analisis_aa():
        def __init__(self,no_analisis,matriz):
            self.no_analisis = no_analisis
            self.matriz = matriz

        def construir(self):    
            self.el = ""
            self.val = ""
            for par in self.matriz:
                self.el+=par[0]+"," 
                self.val+=str(par[1])+"," 
            self.el = self.el[0:-1]
            self.val = self.val[0:-1]
            
        def save(self,conexion):
            self.construir()
            query = """ insert into principal_analisis_aa(no_analisis_id, %s)
            values(%s, %s)""" % (self.el, self.no_analisis, self.val)
            conexion.run_query(query)
            


class Xls_to_db(QMainWindow, Ui_MainWindow):
    def __init__(self,name_file):
        QDialog.__init__(self)
        self.setupUi(self)
        self.bt_choose_file.clicked.connect(self.show_dialog)
        self.bt_load_file.click.connect(self.load_file)

    def show_dialog(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', '/home')
        self.txt_file.setText(fname)

    def load_file(self):
        fname = txt_file.getText()
        self.xls = open_workbook(fname)
        self.db = DB()
        self.process_book()

    def process_book(self):
        for sheet_index in range(self.xls.nsheets):
            sheet = self.xls.sheet_by_index(sheet_index)
            self.process_sheet(sheet)

    def process_sheet(self,sheet):
        sheet_name = sheet.name
        if sheet.ncols < 8 or sheet.nrows < 14:
            logging.info("sheet %s: no se hace nada numero de columnas o filas no cumple" % (sheet_name))
            return 0
        print "procesando: " + sheet_name
        folio = sheet.cell( FOLIO[C], FOLIO[R]).value
        if (folio == "" or folio == None):
            print "no se hace nada para: " + sheet_name  
            return 0
        try:
            folio = folio.split(':')[1]
            folio = folio.strip()
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
        
        if (cliente.upper() == "INTERNO" or cliente == ""): 
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

        lab = sheet.cell(LABORATORISTA[C],LABORATORISTA[R]).value #laboratorista
        des_reporte = sheet.cell(DESCRIPCION_REPORTE[C],DESCRIPCION_REPORTE[R]).value# descripcion reporte
        reporte = Reporte(folio,para, lab, fecha, cliente, des_reporte)
        reporte.save(self.db)
        vacio = 0 # filas vacias encontradas si es mayor a tres los analisis han terminado
        fila_actual = CABECERA + 1 # inicio de analisis
        while vacio < 3 and fila_actual < sheet.nrows:
            try:
                no_analisis = int(sheet.cell(fila_actual,NO_ANALISIS).value)
            except ValueError:
                logging.info("sheet %s: numero de analisis debe ser entero fila %d" 
                                %(sheet_name, fila_actual))
                fila_actual+=1
                continue
            if no_analisis == "":
                vacio+=1
            else:
                des_muestra = sheet.cell(fila_actual, DESCRIPCION_MUESTRA).value
                no_colada = sheet.cell(fila_actual, NO_COLADA).value
                no_muestra = sheet.cell(fila_actual, NO_MUESTRA).value
                muestra = Muestra(no_analisis,folio,no_colada,no_muestra,des_muestra)
                muestra.save(self.db)
                el = 0
                c_vacio = 0
                analisis = []
                while not c_vacio and ANALISIS+el < sheet.ncols:
                    parametro = sheet.cell(CABECERA,ANALISIS+el).value
                    #print  sheet.cell(CABECERA,ANALISIS+el).
                    if parametro == "": 
                        c_vacio = 1
                    else:
                        val = sheet.cell(fila_actual, ANALISIS+el).value
                        try:
                            val = float(val)
                            analisis += [(parametro,val)]
                        except ValueError:
                            pass
                        el += 1
                analisis_aa = Analisis_aa(no_analisis,analisis)
                analisis_aa.save(self.db)
            fila_actual+=1
        obs = ""
        if fila_actual < sheet.nrows:
            obs = sheet.cell(fila_actual, OBSERVACIONES).value
        if obs == "" and fila_actual < sheet.nrows:
            obs = sheet.cell(fila_actual+1, OBSERVACIONES).value
        if not (obs == ""):
            reporte.add_observaciones(obs,self.db)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.processEvents()
    convert = Xls_to_db("./ae2014.xls")
    convert.show()
    sys.exit(app.exec_())


