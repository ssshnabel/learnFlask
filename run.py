from flask import Flask, render_template, request
from datetime import datetime
import sqlite3

app = Flask('my_first_server')
DB_NAME = 'messages.db'

def init_wall_data():
  conn = sqlite3.connect(DB_NAME)
  conn.execute('''create table if not exists wall ( 
            id INTEGER PRIMARY KEY,
            nick TEXT,
            message TEXT)''')
  conn.commit()

def set_wall_data(nick, message):
  conn = sqlite3.connect(DB_NAME)
  conn.execute('insert into wall(nick, message) values(?, ?)', (nick, message))
  conn.commit()

def get_wall_data():
  conn = sqlite3.connect(DB_NAME)
  cursor = conn.execute('select nick, message from wall')
  rows = cursor.fetchall()
  return rows[-1] if rows else (None, None)

def render_main_page():
  cur_datetime_str = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
  wall_data = get_wall_data()
  return render_template('index.html', cur_datetime=cur_datetime_str, nick=wall_data[0], message=wall_data[1])

@app.route('/wall', methods=['POST'])
def response():
  nick = request.form.get("nick")
  message = request.form.get("message")
  set_wall_data(nick, message)
  return render_main_page()

@app.route('/')
def handle_time():
  return render_main_page()

init_wall_data()
app.run(host="0.0.0.0", port="81")
