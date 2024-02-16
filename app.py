from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

# Create a Flask app instance
app = Flask(__name__)

# Set the configuration for the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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

# Check if the script is being executed as the main program
if __name__ == '__main__':
    # Run the Flask app in debug mode
    app.run(debug=True)