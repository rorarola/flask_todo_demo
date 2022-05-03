from flask import Flask,render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired

# Step 1: 載入SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config["SECRET_KEY"] = "i am a hero"
# Step 2: 設定資料庫連線方式
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'

# Step 3: 初始化資料庫
db = SQLAlchemy(app)


class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(200), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    # def __repr__(self):
    #     return '<name %r>' % self.task_name


@app.route("/")
def home():
    task = Tasks.query.order_by(Tasks.date_added).first()
    todo = ""

    if task:
        todo = task.task_name
    return render_template("index.html", todo = todo)

@app.route('/user/<name>')
def user(name):
    return render_template("user.html",name=name)

@app.route('/info')
def info():
    return render_template("info.html")

# Create a form class
class TodoForm(FlaskForm):
    todo = StringField("What do you want to do?", validators=[DataRequired()])
    submit = SubmitField("Submit")


@app.route('/todo', methods=['GET', 'POST'])
def todo():
    form = TodoForm()
    #validate Form
    if form.validate_on_submit():
        task = Tasks(task_name=form.todo.data)
        db.session.add(task)
        db.session.commit()

        todo = form.todo.data
        form.todo.data = ''
        # return render_template("index.html",todo=todo)
    
    todos = Tasks.query.order_by(Tasks.date_added)

    return render_template("todo.html", todos = todos, form = form)

@app.route('/delete_task/<id>')
def delete_task(id):
    task = Tasks.query.get(id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('todo'))