from flask import Flask, request, jsonify, render_template
import sqlite3
import datetime

app = Flask(__name__)

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
    conn = sqlite3.connect('chat.db')
    c = conn.cursor()
    c.execute('DELETE FROM messages')
    conn.commit()
    conn.close()
    return jsonify({"status": "All messages deleted"}), 200

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
