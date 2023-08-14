import pyodbc as db
import configparser
import pandas as pd


class SQL():
    def __init__(self):
        config = configparser.ConfigParser()
        config.read("Database/webconfig")
        driver = config.get("conn", "Driver")
        server = config.get("conn", "Server")
        us = config.get("conn", "Us")
        pw = config.get("conn", "Pwd")
        database = config.get("conn", "Database1")
        self.Cadena = "DRIVER={0};SERVER={1};database={2};UID={3};PWD={4}".format(driver, server, database, us, pw)

    def list_table(self, consulta):
        cn = db.connect(self.Cadena)
        df = pd.read_sql_query(consulta, cn)
        # data = df.to_json(orient="records")
        cn.close()
        # return json.loads(data)
        return df

    def enviarPost(self,consulta):
        try:
            cn = db.connect(self.Cadena)
            cn.autocommit = True
            cursor = cn.cursor()
            cursor.execute(consulta)
            reg = cursor.fetchval()
            # cursor.commit()
            cn.close()
        except db.Error as e:
            print('error', e)
            reg = -1
        return reg