import pymysql.cursors

class Database:
    def runQuery(self, query='', update=False):
        config = {
          'user': 'root',
          'password': '',
          'host': 'localhost',
          'database': 'finance',
          # 'password': '7ngsdDasdfk378hlzp',
          # 'host': 'finance.cgam2wvbif4f.eu-west-1.rds.amazonaws.com',
          # 'database': 'finance',
        }

        conn = pymysql.connect(**config)
        cursor = conn.cursor()

        try:
            cursor.execute(query)
        except pymysql.err.DataError:
            print("Error while executing: "+query)
            raise

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
