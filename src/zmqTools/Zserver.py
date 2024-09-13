import zmq

class Zserver:
    def __init__(self, ip, port):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        self.socket.bind(f"tcp://{ip}:{port}")

    def run(self):
        while True:
            # クライアントからのリクエストを待つ
            message = self.socket.recv_string()
            print(f"Received request: {message}")

            # クライアントに応答を送信
            self.socket.send_string(f"Response: {message}")

if __name__ == "__main__":
    server = Zserver("0.0.0.0", 5001)
    server.run()
