import sqlite3
from datetime import datetime
from .BaseTable import BaseTable

class ChatTable(BaseTable):
    tableName = 'chat'

    def __init__(self, dbName):
        self.dbName = dbName
        super().__init__(self.dbName, self.tableName)

    def create(self):
        createSql = f'''CREATE TABLE IF NOT EXISTS {self.tableName} (
            id INTEGER PRIMARY KEY,
            message TEXT,
            type TEXT,
            timestamp DATETIME
        )'''
        super().create(createSql)

    def insert(self, message, type):
        currTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        super().insert(['message', 'type', 'timestamp'], (message, type, currTime))
