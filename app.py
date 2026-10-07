from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)
DB_PATH = os.path.join(os.path.dirname(__file__), 'todo.db')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            done INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db()
    tasks = conn.execute('SELECT * FROM tasks ORDER BY id DESC').fetchall()
    pending = sum(1 for t in tasks if not t['done'])
    conn.close()
    return render_template('index.html', tasks=tasks, pending=pending)

@app.route('/add', methods=['POST'])
def add():
    title = request.form.get('title', '').strip()
    if title:
        conn = get_db()
        conn.execute('INSERT INTO tasks (title) VALUES (?)', (title,))
        conn.commit()
        conn.close()
    return redirect(url_for('index'))

@app.route('/toggle/<int:task_id>', methods=['POST'])
def toggle(task_id):
    conn = get_db()
    conn.execute('UPDATE tasks SET done = 1 - done WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>', methods=['POST'])
def delete(task_id):
    conn = get_db()
    conn.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

init_db()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
