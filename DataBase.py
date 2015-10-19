#encoding:utf-8
import MySQLdb
import logging

logging.basicConfig(filename='./loginfo.log', level=logging.INFO)
class DB():
    def __init__(self):
        self.DB_HOST = 'localhost' 
        self.DB_USER = 'root' 
        self.DB_PASS = 'root' 
        self.DB_NAME = 'laboratorio'

        datos = [self.DB_HOST, self.DB_USER, self.DB_PASS, self.DB_NAME] 
        self.conn = MySQLdb.connect(*datos)  # Conectar a la base de datos 

    def run_query(self,query):
        print(query)
        cursor = self.conn.cursor()  # Crear un cursor 
        try:
            cursor.execute(query)  # Ejecutar una consulta  
            if query.upper().startswith('SELECT'): 
                data = cursor.fetchall()  # Traer los resultados de un select 
            else:
                self.conn.commit()
                data = None
        except MySQLdb.Error as err:
            logging.error(err[1])
            #logging.error(query)
            data = None
        cursor.close()  # Cerrar el cursor
        return data

    def close(self): 
        self.conn.close()  # Cerrar la conexión 
