from ListProject import db, app
from ListProject.models import Todo, User
from flask import render_template, url_for, redirect, flash, request
from flask_login import login_user, logout_user, login_required
from ListProject.forms import AddForm, RegistrationForm, LoginForm


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have logged out')
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        try:
            form.check_email(form.email)
            form.check_username(form.username)
            user = User(email=form.email.data,
                        username=form.username.data,
                        password=form.password.data)

            db.session.add(user)
            db.session.commit()

        except:
            print('name or email already taken')
            return redirect(url_for('register'))

        flash('Thank you for registering')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.check_password(form.password.data):
            login_user(user)
            flash('log in successful')

            next = request.args.get('next')
            if next == None or next[0] == '/':
                next = url_for('index')

            return redirect(next)

    return render_template('login.html', form=form)


@app.route('/add/', methods=['GET','POST'])
@login_required
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


@app.route('/list/<int:id>')
@login_required
def list(id):
    user = User.query.filter_by(id=id)
    todos = user.tasks
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
