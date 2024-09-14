from flask import Flask, request, jsonify, render_template
import sqlite3
import datetime
import threading
from dbTools.RaptorDB import RaptorDB
from RaptorLinks.Controller import Controller

app = Flask(__name__)
raptorDB = RaptorDB()
raptorDB.init()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send', methods=['POST'])
def send_message():
    message = request.json.get('message')
    message_type = request.json.get('type', 'info')  # デフォルトで 'info' とする
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    raptorDB.chatTable.insert(message, message_type)

    # クライアントからの新しいメッセージを保存
    return jsonify({"status": "Message received"}), 200

@app.route('/send_command', methods=['POST'])
def send_command():
    controller = Controller()
    message    = request.json.get('message')
    response   = controller.sendMessage(message)

    raptorDB.chatTable.insert(response, 'info')

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
        return jsonify({"status": "All messages deleted"}), 200
    except Exception as e:
        return jsonify({"status": "Error", "message": str(e)}), 500

@app.route('/zmq', methods=['GET'])
def zmq_page():
    return render_template('zmq.html')
