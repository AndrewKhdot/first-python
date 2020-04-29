from datetime import datetime

from flask import Flask, render_template, redirect, url_for, request, json
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://postgres:123@localhost/postgres'
db = SQLAlchemy(app)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(1024), unique=True, nullable=False)
    time = db.Column(db.DateTime(), unique=True, nullable=False)

    def __init__(self, text):
        self.text = text
        now = datetime.now()
        self.time = now


db.create_all()


@app.route('/', methods=['GET'])
def hello_world():
    messages = Message.query.all()
    return render_template('index.html', messages=messages)


@app.route('/add_message', methods=['POST'])
def add_message():
    text = request.form['text']
    db.session.add(Message(text))
    db.session.commit()
    return json.dumps({'mess': 'Сообщение сохранено в базе данных'})
