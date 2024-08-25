import sqlite3

class BaseTable():
    def __init__(self, dbName='', tableName=''):
        self.dbName    = dbName
        self.tableName = tableName
        print(f'{self.tableName} table initialized')

    def __del__(self):
        self.conn.close()
        print("Connection closed")

    def _connect(self):
        self.conn   = sqlite3.connect(f'{self.dbName}.db', check_same_thread=True)
        self.cursor = self.conn.cursor()

    def _close(self):
        self.conn.close()

    def _executeSql(self, sql, params=None):
        self._connect()
        if params:
            self.cursor.execute(sql, params)
        else:
            self.cursor.execute(sql)
        self.conn.commit()
        self._close()

    def create(self, createSql):
        self._executeSql(createSql)

    def insert(self, columns, values):
        placeholders = ', '.join('?' * len(values))
        columnNames = ', '.join(columns)
        sql = f"INSERT INTO {self.tableName} ({columnNames}) VALUES ({placeholders})"
        self._executeSql(sql, values)

    def delete(self):
        sql = f'DELETE FROM {self.tableName}'
        self._executeSql(sql)
        print(f'Table "{self.tableName}" deleted')

    def drop(self):
        sql = f'DROP TABLE IF EXISTS {self.tableName}'
        self._executeSql(sql)
        print(f'Table "{self.tableName}" dropped')

    def selectAll(self):
        self._connect()
        self.cursor.execute(f'''
            SELECT 
                *
            FROM {self.tableName}
            LIMIT 1000
        ''')
        res = self.cursor.fetchall()
        self._close()
        return res
