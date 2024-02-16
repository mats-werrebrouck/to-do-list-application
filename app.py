from flask import Flask, render_template, request, redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy
import secrets

# Generate a secure random key
secret_key = secrets.token_hex(16)

# Create a Flask app instance
app = Flask(__name__)

# Set the configuration for the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = secret_key

# Create an instance of SQLAlchemy and bind it to the app
db = SQLAlchemy(app)
app.app_context().push()

# Create a model for the 'todo' table in the database
class Todo(db.Model):
    # Define the columns of the table
    id = db.Column(db.Integer, primary_key=True) # Primary key for the table
    task_name = db.Column(db.String(200), nullable=False) # Task name column (text with max length of 200 characters)
    completed = db.Column(db.Boolean, default=False) # Completed column (boolean, default is False)

# Create the 'todo' table in the database if it doesn't exist
db.create_all()

def is_duplicate_task(task_name):
    for task in Todo.query.all():
        if task.task_name == task_name:
            return True
    return False

# Define a route for the root URL with support for GET and POST methods
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # If the request method is POST (from submission), extract the task_name from the form data
        task_name = request.form['task_name']

        # Create a new 'Todo' object with the task_name and default completed status as False
        new_task = Todo(task_name=task_name, completed=False)

        # Add the new_task object to the database session
        db.session.add(new_task)
        
        # Commit the changes to the database, effectively inserting the new_task into the 'todo' table
        db.session.commit()

    # Retrieve all tasks from the 'todo' table
    tasks = Todo.query.all()

    # Render the 'index.html' template and pass the tasks to it
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
                return render_template('index.html', tasks=Todo.query.all())
        return render_template('edit.html', task=task_to_edit)
    else:
        return render_template('index.html', tasks=Todo.query.all())

@app.route('/delete/<int:id>', methods=['POST'])
def delete_task(id):
    # Get the task with the specified ID from the database
    task = Todo.query.get(id)

    # Delete the task from the database
    db.session.delete(task)

    # Commit the changes to the database
    db.session.commit()

    # Redirect the user to the root URL
    return redirect('/')

# Check if the script is being executed as the main program
if __name__ == '__main__':
    # Run the Flask app in debug mode
    app.run(debug=True)