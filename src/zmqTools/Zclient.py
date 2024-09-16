import zmq

class Zclient:
    def __init__(self, ip, port, topic):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)  # Use REQ for request-reply pattern
        self.socket.connect(f"tcp://{ip}:{port}")
        self.topic = topic

    def request(self, msg):
        # Send a message to the server with a topic
        self.socket.send_string(f"{self.topic}${msg}")

        # Wait for the server's reply
        reply = self.socket.recv_string()
        parts = reply.split('$', 1)
        if len(parts) == 2:
            reply_topic, reply_message = parts
            return reply_message
        else:
            return reply        
        return reply

    def close(self):
        self.socket.close()
        self.context.term()

    def __del__(self):
        self.close()

if __name__ == "__main__":
    client = Zclient("dev", 5001, "ZSERVER")
    res = client.request("Hello from Python!")
    print(f"Received reply: {res}, {type(res)}")
