from SampleDB import SampleDB

if __name__ == '__main__':
    sampleDb = SampleDB()
    print(sampleDb.counterTable.drop())
    print(sampleDb.temperatureTable.drop())