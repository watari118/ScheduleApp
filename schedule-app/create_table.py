import sqlite3

# データベースへの接続
conn = sqlite3.connect('schedule.db')
c = conn.cursor()

# テーブルの作成
c.execute('''CREATE TABLE schedules
             (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, date TEXT, description TEXT)''')

# 変更の反映
conn.commit()

# 接続の終了
conn.close()
