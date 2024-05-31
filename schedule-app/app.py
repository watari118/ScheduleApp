from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Databaseの設定
DATABASE = 'schedule.db'

# データベースへの接続
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# スケジュールの一覧表示
@app.route('/')
def index():
    conn = get_db_connection()
    schedules = conn.execute('SELECT * FROM schedules').fetchall()
    conn.close()
    return render_template('index.html', schedules=schedules)

# 新規スケジュールの追加
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        title = request.form['title']
        date = request.form['date']
        description = request.form['description']
        
        conn = get_db_connection()
        conn.execute('INSERT INTO schedules (title, date, description) VALUES (?, ?, ?)',
                     (title, date, description))
        conn.commit()
        conn.close()
        
        return redirect(url_for('index'))
    
    return render_template('add.html')

# スケジュールの編集
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = get_db_connection()
    schedule = conn.execute('SELECT * FROM schedules WHERE id = ?', (id,)).fetchone()
    conn.close()
    
    if request.method == 'POST':
        title = request.form['title']
        date = request.form['date']
        description = request.form['description']
        
        conn = get_db_connection()
        conn.execute('UPDATE schedules SET title = ?, date = ?, description = ? WHERE id = ?',
                     (title, date, description, id))
        conn.commit()
        conn.close()
        
        return redirect(url_for('index'))
    
    return render_template('edit.html', schedule=schedule)

# スケジュールの削除
@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM schedules WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True) 
