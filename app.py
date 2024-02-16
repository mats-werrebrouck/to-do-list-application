from flask import Flask, render_template, request, redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy
import secrets

secret_key = secrets.token_hex(16)

# Create a Flask app instance
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = secret_key

# Create an instance of SQLAlchemy and bind it to the app
db = SQLAlchemy(app)
app.app_context().push()

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)

# Create the 'todo' table in the database if it doesn't exist
db.create_all()

def is_duplicate_task(task_name):
    for task in Todo.query.all():
        if task.task_name == task_name:
            return True
    return False

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        task_name = request.form['task_name']
        if not is_duplicate_task(task_name) and task_name != '':
            new_task = Todo(task_name=task_name, completed=False)
            db.session.add(new_task)
            db.session.commit()

    tasks = Todo.query.all()
    return render_template('index.html', tasks=tasks)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_task(id):
    task_to_edit = next((task for task in Todo.query.all() if task.id == id), None)

    if task_to_edit:
        if request.method == 'POST':
            new_task_name = request.form['task_name']
            if not is_duplicate_task(new_task_name):
                task_to_edit.task_name = new_task_name
                db.session.commit()
                return redirect('/')
        return render_template('edit.html', task=task_to_edit)
    else:
        return redirect('/')

@app.route('/delete/<int:id>', methods=['POST'])
def delete_task(id):
    task = Todo.query.get(id)
    db.session.delete(task)
    db.session.commit()
    return redirect('/')

# Check if the script is being executed as the main program
if __name__ == '__main__':
    # Run the Flask app in debug mode
    app.run(debug=True)