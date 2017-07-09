import mysql.connector

class database:
    def runQuery(self, query=''):
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
        else:
            conn.commit()              #Commit the data
            data = None

        cursor.close()
        conn.close()

        return data
