import time
from flask import Flask,render_template,url_for,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self):
        return '<Task %r' % self.id


@app.route('/', methods=['POST','GET'])#adding get and post methods to add and delte tasks
def index():
    if request.method == 'POST':
        task_content = request.form['content']#task content is the content typed in the text box the request.form for the form we created and its id which is content
        new_task = Todo(content = task_content)#object of our todo model and now we have to push it to the databse
        if len(task_content) < 1 :
            return redirect('/')
        else:
            try:
                db.session.add(new_task) #put the task to the database
                db.session.commit()#the commit it to the database 
                return redirect('/')#then we will redirect to homepage after its done import redirect on top
            except:
                return 'There was a problem adding the task'
    
    else:
        tasks = Todo.query.order_by(Todo.date_created).all() #is going to look at all the database content in the order they were created
        return render_template('index.html', tasks = tasks)#sending it to our template


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'DElETE operation unsucessfull'


@app.route('/update/<int:id>', methods = ['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == "POST":
        task.content  =request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'UPDATE error'

    else:
        return render_template('update.html', task=task)

if __name__ == "__main__":
    app.run(debug=True)