from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, UTC

app = Flask(__name__) #references this file
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db' #3 slash is rel path while 4 is abs path
db= SQLAlchemy(app) #initialized db  with settingsfrom app


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(200), nullable = False) #no null task 
    date_created= db.Column(db.DateTime, default=datetime.now(UTC))
    
    
    def __repr__(self):
        return '<Task %r>' % self.id #returns id of task created after everytime a tsk is created

@app.route('/', methods=['POST', 'GET']) #methods the route can accept
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)
        
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'Issue in adding task'
        
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)
    
    
@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'Problem in delete route'
    
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content']
        
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'Problem in update'
    else:
        return render_template('update.html', task=task)
    

if __name__ == '__main__':
    app.run(debug=True)  #if we have any errors, they will pop in browser
    
    
