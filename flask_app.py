from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["DEBUG"] = True

SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="apapusia",
    password="Mug4rra.1888",
    hostname="apapusia.mysql.pythonanywhere-services.com",
    databasename="apapusia$tododb",
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Todo(db.Model):

    __tablename__ = "todos"

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200))
    complete = db.Column(db.Boolean)

@app.route('/')
def index():
    incomplete = Todo.query.filter_by(complete=False).all()
    complete = Todo.query.filter_by(complete=True).all()

    return render_template('main.html', incomplete=incomplete, complete=complete)


@app.route('/add', methods=['POST'])
def add():
    todo = Todo(text=request.form['todoitem'], complete=False)
    db.session.add(todo)
    db.session.commit()

    return redirect(url_for('index'))


@app.route('/complete/<id>')
def complete(id):

    todo = Todo.query.filter_by(id=int(id)).first()
    todo.complete = True
    db.session.commit()

    return redirect(url_for('index'))