from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from models import db, Goal, Task

app = Flask(__name__)
# connecting database

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://prince_user:password@localhost/goals'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
with app.app_context():
    db.create_all()

# routes

# Adding goals route

# display goals
@app.route('/goals')
def display_goals():
    Goals = Goal.query.all()
    return render_template('goals.html', Goals=Goals)

#add goals 
@app.route('/goals', methods=['POST', 'GET'])
def add_goals():
    if request.method == 'POST':
        goal_name = request.form.get('goal_name')
        if goal_name != '':
            new = Goal(goals=goal_name)
            db.session.add(new)
            db.session.commit()
            return redirect('/goals')
    else:
        return redirect('/goals')
# delte goals
@app.route('/goals/delete/<int:id>', methods=['POST'])
def delete_goals(id):
    if request.method == 'POST':
        goal = Goal.query.get(id)
        if goal:
            db.session.delete(goal)
            db.session.commit()
            return redirect('/goals')
        else:
            return redirect('/goals')

# complete goals
@app.route('/goals/completed/<int:id>' , methods=["POST"])
def complete_goals(id):
    if request.method == 'POST':
        goal = Goal.query.get(id)
        if goal:
            goal.completed = True
            db.session.commit()
            return redirect('/goals')
        else:
            return redirect('/goals')



# Function to add and display tasks 
@app.route('/' , methods=['GET', 'POST'])
def home():
    Tasks = Task.query.all()
    return render_template('home.html', Tasks=Tasks)

def add_task():
    if request.method == 'POST':
        task_name = request.form.get('task_name')
        if task_name != '':
            new = Task(Taskk=task_name)
            db.session.add(new)
            db.session.commit()
            return redirect('/')
    else:
        return redirect('/')
    


# Remove task function 
@app.route('/task/delete/<int:id>', methods=['POST'])
def erase(id):
    if request.method == 'POST':       
        task = Task.query.get(id)
        if task:
            db.session.delete(task)
            db.session.commit()
        return redirect('/')


# Completed function 
@app.route('/task/completed/<int:id>', methods=['POST'])
def complete(id):
    if request.method == 'POST':
        task = Task.query.get(id)
        if task:
            task.completed = True
            db.session.commit()
        return redirect('/')




if __name__ == '__main__':
    app.run(debug=True)
