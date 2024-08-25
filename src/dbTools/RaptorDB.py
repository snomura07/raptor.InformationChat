import sqlite3
from .table.CounterTable import CounterTable
from .table.TemperatureTable import TemperatureTable
from .table.ChatTable import ChatTable

class RaptorDB():
    dbName = 'raptor'

    def __init__(self):
        self.counterTable     = CounterTable(self.dbName)
        self.temperatureTable = TemperatureTable(self.dbName)
        self.chatTable        = ChatTable(self.dbName)

    def init(self):
        self.counterTable.create()
        self.temperatureTable.create()
        self.chatTable.create()
