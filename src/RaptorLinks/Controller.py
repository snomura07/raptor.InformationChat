import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from openaiTools.Assistant import Assistant
from zmqTools.

class Controller():
    def __init__(self):
        assistant = Assistant()

    def sendMessage(self, msg):
        pass

if __name__ == "__main__":
    print('ok')
