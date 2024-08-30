const socket = io();
socket.on('new_message', function(data) {
    addMessage(data);
});

socket.on('all_deleted', function() {
    document.getElementById('messages').innerHTML = '';
});

function addMessage(msg) {
    const messagesContainer = document.getElementById('messages');

    const messageElement = document.createElement('div');
    const messageType = msg.type || 'info';
    messageElement.className = 'message ' + messageType;

    const textElement = document.createElement('div');
    textElement.textContent = msg.message;

    const timestampElement = document.createElement('div');
    timestampElement.className = 'timestamp';
    timestampElement.textContent = msg.timestamp;

    messageElement.appendChild(textElement);
    messageElement.appendChild(timestampElement);
    messagesContainer.appendChild(messageElement);

    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function loadMessages() {
    fetch('/messages')
    .then(response => response.json())
    .then(data => {
        const messagesContainer = document.getElementById('messages');
        messagesContainer.innerHTML = ''; // 古いメッセージをクリア

        data.forEach(msg => {
            addMessage(msg);
        });
    })
    .catch(error =>console.error('Error loading messages:', error));
}

// ページロード時にメッセージを読み込む
window.onload = function() {
    loadMessages();
};

document.getElementById('send-button').addEventListener('click', () => {
    const input = document.getElementById('message-input');
    const message = input.value;
    const messageType = 'info'; // ここで 'info' か 'error' を選択するロジックを追加できます
    fetch('/send', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message, type: messageType }),
    }).then(() => {
        input.value = '';
    });
});

document.getElementById('delete-button').addEventListener('click', () => {
    if (confirm('本当に全メッセージを削除しますか？')) {
        fetch('/delete_all', {
            method: 'DELETE',
        }).then(() => {
            document.getElementById('messages').innerHTML = '';
        }).catch(error =>console.error('Error:', error));
    }
});

// WebSocketの接続を初期化
socket.on('connect', function() {
    console.log('WebSocket connection established');
});

// メニューの表示/非表示を切り替える
document.getElementById('menu-button').addEventListener('click', () => {
    const menuList = document.getElementById('menu-list');
    menuList.classList.toggle('show');
});

// メニュー外をクリックしたときにメニューを閉じる
window.addEventListener('click', function(event) {
    const menuList = document.getElementById('menu-list');
    const menuButton = document.getElementById('menu-button');
    if (!menuButton.contains(event.target) && !menuList.contains(event.target)) {
        menuList.classList.remove('show');
    }
});