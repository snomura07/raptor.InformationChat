import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from openaiTools.Assistant import Assistant
from zmqTools.Zclient import Zclient

class Controller():
    def __init__(self):
        self.assistant = Assistant()
        self.zclient   = Zclient("dev", 5001, "ZSERVER")

    def sendMessage(self, msg):
        assistantResponse = self.assistant.createAndPoll(msg)
        zclientResponse   = self.zclient.request(assistantResponse)
        return zclientResponse

if __name__ == "__main__":
    print('ok')
