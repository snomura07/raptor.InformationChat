import sqlite3

class TestDb:
    def __init__():
        conn = sqlite3.connect('test.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS sample (
            id INTEGER PRIMARY KEY,
            message TEXT,
            timestamp DATETIME
        )''')

        conn.commit()
        conn.close()

    def insert():
        conn = sqlite3.connect('test.db')
        c = conn.cursor()
        message = 'ggg'
        timestamp = '2024-08-25 12:00:12'
        c.execute(f'INSERT INTO sample (message, timestamp) VALUES ("{message}", "{timestamp}")')
        conn.commit()
        conn.close()


def selectSample():
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    c.execute('SELECT id, message, timestamp FROM sample')
    messages = [{"id": row[0], "message": row[1], "timestamp": row[2]} for row in c.fetchall()]
    conn.close()
    return messages

if __name__ == '__main__':
    init_db()
    insertSample()

    print(selectSample())
