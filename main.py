from datetime import datetime
from flask import Flask, render_template, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from forms import AddForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.sqlite"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

###############################
#    DATABASE SECTION         #
###############################

class Todo(db.Model):
    __tablename__ = 'todos'

    date = datetime.utcnow()

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30))
    description = db.Column(db.Text)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    last_edited = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, title, description):
        self.title = title
        self.description = description

    def __repr__(self):
        return self.id

    def render_todo(self):
        return {'id': self.id,
                'title': self.title,
                'description': self.description,
                'post_date': self.date_posted,
                'last_edited': self.last_edited}



################################
#        Routes                #
################################

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/add/', methods=['GET','POST'])
def add():
    form = AddForm()
    if form.validate_on_submit():
        title = form.title.data
        desc = form.description.data
        
        new_todo = Todo(title, desc)

        db.session.add(new_todo)
        db.session.commit()
        
        flash('new item added successfully')
        return redirect(url_for('list'))

    return render_template('add.html', form=form)

@app.route('/list')
def list():
    todos = Todo.query.all()
    todo_list = []
    for todo in todos:
        n_todo = todo.render_todo()
        todo_list.append(n_todo)

    return render_template('list.html', todo_list=todo_list)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    form = AddForm()
    todo = Todo.query.get(id)

    if todo:
        if form.validate_on_submit():
            todo.title = form.title.data
            todo.description = form.description.data
            todo.last_edited = datetime.utcnow()
            db.session.commit()
            flash('Item has been updated succesfully')
            return redirect(url_for('list'))

        form.title.data = todo.title
        form.description.data = todo.description
        return render_template('edit.html', form=form)

@app.route('/delete/<int:id>')
def delete(id):
    todo = Todo.query.get(id)

    db.session.delete(todo)
    db.session.commit()
    
    flash('item deleted successfully')

    return redirect(url_for('list'))
if __name__ == '__main__':
    app.run(debug=True)