from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from models import db, Goal, Task

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://prince_user:password@localhost/store'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    Tasks = Task.query.all()
    return render_template('home.html', Tasks=Tasks)

@app.route('/add' , methods=['POST'])
def add_task():
    task_name = request.form.get('task_name')
    if task_name != '':
        new = Task(task_name=task_name)
        db.session.add(new)
        db.session.commit()
        return redirect('/')
    else:
        return redirect('/')
    
if __name__ == '__main__':
    app.run(debug=True)
