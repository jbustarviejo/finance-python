import mysql.connector

class Database:
    def runQuery(self, query='', update=False):
        config = {
          'user': 'root',
          'password': '',
          'host': '127.0.0.1',
          'database': 'finance',
          'raise_on_warnings': True,
        }

        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        cursor.execute(query)

        if query.upper().startswith('SELECT'):
            data = cursor.fetchall()   # get results from select
            if(not data): return False
            if update: #IF also update at the same time
                cursor2 = conn.cursor()
                cursor2.execute("UPDATE "+update["table"]+" SET "+update["column"]+" = NOW() WHERE id ="+str(data[0][0]))
                conn.commit()
                cursor2.close()
        else:
            #Commit the data
            conn.commit()
            data = None

        cursor.close()
        conn.close()

        return data
