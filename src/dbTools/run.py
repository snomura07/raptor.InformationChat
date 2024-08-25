from RaptorDB import RaptorDB

if __name__ == '__main__':
    raptorDB = RaptorDB()
    print(raptorDB.counterTable.selectAll())
    print(raptorDB.temperatureTable.selectAll())

    raptorDB.counterTable.insert(123)
    raptorDB.temperatureTable.insert(23.6)
