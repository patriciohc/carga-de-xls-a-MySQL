import MySQLdb

DB_HOST = 'localhost' 
DB_USER = 'root' 
DB_PASS = 'root' 
DB_NAME = 'laboratorio' 


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
