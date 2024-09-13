from Zclient import Zclient
import time

if __name__ == '__main__':
    zclient = Zclient('localhost', 5001, 'ZIMAGE')

    while True:
        zclient.send('test')
        time.sleep(1)
