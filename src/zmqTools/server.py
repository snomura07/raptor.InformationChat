import zmq

if __name__ == '__main__':
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.bind("tcp://*:5001")
    topic = "ZIMAGE"
    socket.setsockopt_string(zmq.SUBSCRIBE, topic)

    while True:
        message = socket.recv_string()
        print(f"Received message: {message}")
