import sqlite3
from datetime import datetime
from .BaseTable import BaseTable

class TemperatureTable(BaseTable):
    tableName = 'temperature'

    def __init__(self, dbName):
        self.dbName = dbName
        super().__init__(self.dbName, self.tableName)

    def create(self):
        createSql = f'''CREATE TABLE IF NOT EXISTS {self.tableName} (
            id INTEGER PRIMARY KEY,
            temperature REAL,
            timestamp DATETIME
        )'''
        super().create(createSql)

    def insert(self, temperature):
        currTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        super().insert(['temperature', 'timestamp'], (temperature, currTime))
