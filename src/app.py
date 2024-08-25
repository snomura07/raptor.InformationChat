from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO, emit
import sqlite3
import datetime
import threading
import zmq

app = Flask(__name__)
socketio = SocketIO(app)

def init_db():
    conn = sqlite3.connect('chat.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY, message TEXT, timestamp TEXT, type TEXT)''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send', methods=['POST'])
def send_message():
    message = request.json.get('message')
    message_type = request.json.get('type', 'info')  # デフォルトで 'info' とする
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    conn = sqlite3.connect('chat.db')
    c = conn.cursor()
    c.execute('INSERT INTO messages (message, timestamp, type) VALUES (?, ?, ?)', (message, timestamp, message_type))
    conn.commit()
    conn.close()

    # 新しいメッセージが来たらクライアントに通知
    socketio.emit('new_message', {'message': message, 'timestamp': timestamp, 'type': message_type})
    return jsonify({"status": "Message received"}), 200

@app.route('/messages', methods=['GET'])
def get_messages():
    conn = sqlite3.connect('chat.db')
    c = conn.cursor()
    c.execute('SELECT message, timestamp, type FROM messages')
    messages = [{"message": row[0], "timestamp": row[1], "type": row[2]} for row in c.fetchall()]
    conn.close()
    return jsonify(messages), 200

@app.route('/delete_all', methods=['DELETE'])
def delete_all_messages():
    try:
        conn = sqlite3.connect('chat.db')
        c = conn.cursor()
        c.execute('DELETE FROM messages')
        conn.commit()
        conn.close()
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
    init_db()
    zmq_thread = threading.Thread(target=zmq_server)
    zmq_thread.start()
    socketio.run(app, host='0.0.0.0', port=5000)
