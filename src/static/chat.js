function addMessage(msg) {
    const messagesContainer = document.getElementById('messages');

    const messageElement = document.createElement('div');
    const messageType = msg.type || 'info';
    messageElement.className = 'message ' + messageType;
    messageElement.id = msg.id || '';  // IDを追加

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
    loadMessagesInterval = setInterval(loadMessages, 1000);  // 1秒ごとにメッセージを更新
};

document.getElementById('send-button').addEventListener('click', () => {
    const input = document.getElementById('message-input');
    const message = input.value;
    const messageType = 'sent';

    // 入力されたメッセージをまず表示
    const userMessage = {
        message: message,
        type: messageType,
        timestamp: formatDate(new Date())
    };
    addMessage(userMessage);  // ユーザーが送信したメッセージをチャットに追加
    input.value = '';  // 入力フィールドをクリア

    // 入力フィールドをクリア
    input.value = '';
    clearInterval(loadMessagesInterval);  // メッセージ送信中はリロードを一時停止

    fetch('/send', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message, type: messageType }),
    }).then(() => {
        // 「...」をinfoメッセージとして表示
        const temporaryMessageId = 'temp-info-' + Date.now();
        const temporaryMessage = {
            id: temporaryMessageId,
            message: '...',
            type: 'info',
            timestamp: new Date().toISOString()
        };
        addMessage(temporaryMessage);

        // /send_command APIを呼び出す
        return fetch('/send_command', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message, type: messageType }),
        }).then(() => {
            console.log('コマンドが正常に送信されました');
            // 一時メッセージを削除
            removeTemporaryMessage(temporaryMessageId);
            // メッセージを再読み込み
            loadMessages();
        }).catch(error => {
            console.error('Error sending command:', error);
            removeTemporaryMessage(temporaryMessageId);  // エラー時にも削除
        });
    }).catch(error => {
        console.error('Error sending message:', error);
    });
});

function formatDate(date) {
    const year = date.getFullYear();
    const month = ('0' + (date.getMonth() + 1)).slice(-2);  // 月は0始まりなので+1
    const day = ('0' + date.getDate()).slice(-2);
    const hours = ('0' + date.getHours()).slice(-2);
    const minutes = ('0' + date.getMinutes()).slice(-2);
    const seconds = ('0' + date.getSeconds()).slice(-2);
    return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
}

// 一時メッセージを削除する関数
function removeTemporaryMessage(id) {
    const messageElement = document.getElementById(id);
    if (messageElement) {
        messageElement.remove();  // メッセージを削除
    }
}

document.getElementById('delete-button').addEventListener('click', () => {
    if (confirm('本当に全メッセージを削除しますか？')) {
        fetch('/delete_all', {
            method: 'DELETE',
        }).then(() => {
            document.getElementById('messages').innerHTML = '';
        }).catch(error =>console.error('Error:', error));
    }
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

document.getElementById('message-input').addEventListener('keypress', (event) => {
    if (event.key === 'Enter') {
        event.preventDefault();
        document.getElementById('send-button').click();
    }
});
