import sqlite3
from table.CounterTable import CounterTable
from table.TemperatureTable import TemperatureTable

class SampleDB():
    dbName = 'sample'

    def __init__(self):
        self.counterTable     = CounterTable(self.dbName)
        self.temperatureTable = TemperatureTable(self.dbName)
