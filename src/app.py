from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO, emit
import sqlite3
import datetime
import threading
import zmq
from dbTools.RaptorDB import RaptorDB

app      = Flask(__name__)
socketio = SocketIO(app)
raptorDB = RaptorDB()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send', methods=['POST'])
def send_message():
    message = request.json.get('message')
    message_type = request.json.get('type', 'info')  # デフォルトで 'info' とする
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    raptorDB.chatTable.insert(message, message_type)

    # 新しいメッセージが来たらクライアントに通知
    socketio.emit('new_message', {'message': message, 'timestamp': timestamp, 'type': message_type})
    return jsonify({"status": "Message received"}), 200

@app.route('/messages', methods=['GET'])
def get_messages():
    res = raptorDB.chatTable.selectAll()
    messages = [{"id":row[0], "message": row[1], "type": row[2], "timestamp": row[3]} for row in res]
    return jsonify(messages), 200

@app.route('/delete_all', methods=['DELETE'])
def delete_all_messages():
    try:
        raptorDB.chatTable.delete()
        socketio.emit('all_deleted')
        return jsonify({"status": "All messages deleted"}), 200
    except Exception as e:
        return jsonify({"status": "Error", "message": str(e)}), 500

@app.route('/zmq', methods=['GET'])
def zmq_page():
    return render_template('zmq.html')

def zmq_server():
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.bind("tcp://*:5001")
    topic = "ZIMAGE"
    socket.setsockopt_string(zmq.SUBSCRIBE, topic)  # サブスクライブするトピックを設定

    while True:
        message = socket.recv_string()
        print(f"Received message: {message}")

        # メッセージをパースして必要に応じて処理
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        socketio.emit('zmq_message', {'message': message, 'timestamp': timestamp, 'type': 'zmq'})

if __name__ == '__main__':
    raptorDB.init()

    zmq_thread = threading.Thread(target=zmq_server)
    zmq_thread.start()
    socketio.run(app, host='0.0.0.0', port=5000)
