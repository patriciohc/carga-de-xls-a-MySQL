#encoding:utf-8

class Registro():
    def __init__(self,no_analisis, nombre = 'ESCORIA DE FUNDICION'):
        self.no_analisis = int(no_analisis)
        self.nombre = nombre

    def save(self,conexion):
        query = """ insert into registro(ID_ANALISIS, NOMBRE)
                     values(%s,'%s')""" % (self.no_analisis, self.nombre)
        conexion.run_query(query)


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
                insert into reporte(FOLIO, PARA, ANALISTA, FECHA, 
                CLIENTE, DESCRIPCION, OBSERVACIONES) values('%s', '%s', '%s',
                '%s', '%s','%s','%s')""" % (self.folio, self.para, 
                self.laboratorista, self.fecha, self.cliente, self.descripcion, 
                self.observaciones)
        conexion.run_query(query)

    def add_observaciones(self,conexion, observaciones):
        query = """ UPDATE reporte SET OBSERVACIONES='%s' 
            WHERE FOLIO='%s' """ % (observaciones, self.folio) 
        conexion.run_query(query)


class Escoria():
    def __init__(self,no_analisis,folio_reporte,no_colada,descripcion):
        self.no_analisis = int(no_analisis)
        try:
            folio_reporte = int(folio_reporte)
            no_colada = int(no_colada)
        except ValueError:
            pass
        self.folio_reporte = str(folio_reporte)
        self.no_colada = str(no_colada)
        self.descripcion = descripcion

    def save(self,conexion):
        query = """ insert into escoria(ID_ANALISIS, FOLIO_REPORTE,
                    NO_COLADA, DESCRIPCION) values(%s, 
                    '%s', '%s', '%s', %d)""" % (self.no_analisis, 
                    self.folio_reporte, self.no_colada, 
                    self.descripcion)
        conexion.run_query(query)


class AnalisisEscoria():
        def __init__(self,no_analisis,datos):
            self.no_analisis = no_analisis
            self.datos = datos

        def construir(self):
            self.parametro = ""
            self.value = ""
            for par in self.datos:
                self.parametro += par['parametro']+"," 
                self.value += str(par['value'])+"," 
            self.parametro = self.parametro[0:-1]
            self.value = self.value[0:-1]
            
        def save(self,conexion):
            self.construir()
            query = """ insert into analisis_escoria(ID_ANALISIS, %s)
            values(%s, %s)""" % (self.parametro, self.no_analisis, self.value)
            conexion.run_query(query)
