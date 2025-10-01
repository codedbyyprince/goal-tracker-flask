from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from models import db, Goal, Task

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://prince_user:password@localhost/goals'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

# ------------------ GOALS ROUTES ------------------

# Display goals
@app.route('/goals')
def display_goals():
    # Only show goals that are not completed
    Goals = Goal.query.filter(Goal.completed == False).all()
    return render_template('goals.html', Goals=Goals)

# Add a new goal
@app.route('/goals', methods=['POST', 'GET'])
def add_goals():
    if request.method == 'POST':
        goal_name = request.form.get('goal_name')
        if goal_name != '':
            new = Goal(goals=goal_name)
            db.session.add(new)
            db.session.commit()
    return redirect('/goals')

# Delete a goal
@app.route('/goals/delete/<int:id>', methods=['POST'])
def delete_goals(id):
    goal = Goal.query.get(id)
    if goal:
        db.session.delete(goal)
        db.session.commit()
    return redirect('/goals')

# Mark a goal as completed
@app.route('/goals/completed/<int:id>', methods=['POST'])
def complete_goals(id):
    goal = Goal.query.get(id)
    if goal:
        goal.completed = True
        db.session.commit()
    return redirect('/goals')

# ------------------ TASKS ROUTES ------------------

# Tasks page
@app.route('/', methods=['GET', 'POST'])
def home():
    # Only show incomplete tasks
    Tasks = Task.query.filter(Task.completed == False).all()
    # Pass goals for the dropdown (for task creation)
    Goals = Goal.query.filter(Goal.completed == False).all()
    return render_template('home.html', Tasks=Tasks, Goals=Goals)

# Add a task
@app.route('/task', methods=['POST'])
def add_task():
    task_name = request.form.get('task_name')
    goal_id = request.form.get('goals')  # Convert string to int
    if goal_id == "":
        goal_id = None
    else:
        goal_id = int(goal_id)
    if task_name != '':
        new = Task(Taskk=task_name, Goal_id=goal_id)
        db.session.add(new)
        db.session.commit()
    return redirect('/')

# Delete a task
@app.route('/task/delete/<int:id>', methods=['POST'])
def erase(id):
    task = Task.query.get(id)
    if task:
        db.session.delete(task)
        db.session.commit()
    return redirect('/')

# Mark a task as completed
@app.route('/task/completed/<int:id>', methods=['POST'])
def complete(id):
    task = Task.query.get(id)
    if task:
        task.completed = True
        db.session.commit()
    return redirect('/')

@app.route('/completed_tasks', methods=['GET'])
def completed_tasks():
    tasks = Task.query.filter(Task.completed == True).all()
    return render_template('completed_tasks.html', tasks=tasks)

@app.route('/completed_task/delete/<int:id>', methods=['POST'])
def remove_completed_task(id):
    task = Task.query.get(id)
    if task:
        db.session.delete(task)
        db.session.commit()
    return redirect('/completed_tasks')



@app.route('/completed_goals', methods=['GET'])
def completed_goals():
    goals = Goal.query.filter(Goal.completed == True).all()
    return render_template('completed_goals.html', goals=goals)

@app.route('/completed_goals/delete/<int:id>', methods=['POST'])
def remove_completed_goal(id):
    goal = Goal.query.get(id)
    if goal:
        db.session.delete(goal)
        db.session.commit()
    return redirect('/completed_goals')

# ------------------ GOAL PROGRESS ------------------

@app.route('/goals/<int:goal_id>/tasks', methods=['GET'])
def goal_info(goal_id):
    # Fetch the goal
    goal = Goal.query.get_or_404(goal_id)
    # Fetch tasks belonging to that goal
    tasks = Task.query.filter_by(Goal_id=goal.id).all()
    return render_template('info.html', goal=goal, tasks=tasks)

# ------------------ RUN APP ------------------

if __name__ == '__main__':
    app.run(debug=True)
