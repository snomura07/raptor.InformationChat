import sqlite3
from datetime import datetime
from .BaseTable import BaseTable

class CounterTable(BaseTable):
    tableName = 'counter'

    def __init__(self, dbName):
        self.dbName = dbName
        super().__init__(self.dbName, self.tableName)

    def create(self):
        createSql = f'''CREATE TABLE IF NOT EXISTS {self.tableName} (
            id INTEGER PRIMARY KEY,
            count UNSIGNED INTEGER,
            timestamp DATETIME
        )'''
        super().create(createSql)

    def insert(self, count):
        currTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        super().insert(['count', 'timestamp'], (count, currTime))
