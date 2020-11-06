from ListProject import db, app
from ListProject.models import Todo, User
from flask import render_template, url_for, redirect, flash, request, abort
from flask_login import login_user, logout_user, login_required, current_user
from ListProject.forms import AddForm, RegistrationForm, LoginForm


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have logged out', 'success')
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)

        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data} successfully', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.check_password(form.password.data):
            login_user(user)
            flash('log in successful', 'success')

            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
            # if next == None or next[0] == '/':
            #     next = url_for('index')
            #     return redirect(next)
        else:
            flash('Log in unsuccessful. Check email and password', 'danger')

    return render_template('login.html', form=form)


@app.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = AddForm()
    if form.validate_on_submit():
        title = form.title.data
        desc = form.description.data

        new_todo = Todo(title, desc, user_id=current_user.id)

        db.session.add(new_todo)
        db.session.commit()

        flash('new item added successfully', 'success')
        return redirect(url_for('list', user_id=current_user.id))

    return render_template('add.html', form=form)


@app.route('/list/<int:user_id>')
@login_required
def list(user_id):
    user = User.query.get_or_404(user_id)
    todos = user.tasks
    todo_list = []
    for todo in todos:
        n_todo = todo.render_todo()
        todo_list.append(n_todo)

    return render_template('list.html', todo_list=todo_list)


@app.route('/todo/<int:todo_id>/edit', methods=['GET', 'POST'])
def edit(todo_id):
    form = AddForm()
    todo = Todo.query.get_or_404(todo_id)

    if todo.user_id != current_user.id:
        abort(403)

    if form.validate_on_submit():
        todo.title = form.title.data
        todo.description = form.description.data
        db.session.commit()
        flash('Item has been updated succesfully', 'success')
        return redirect(url_for('list', user_id=current_user.id))
    elif request.method == 'GET':
        form.title.data = todo.title
        form.description.data = todo.description

    return render_template('edit.html', form=form)


@app.route('/todo/<int:todo_id>/delete')
@login_required
def delete(todo_id):
    todo = Todo.query.get_or_404(todo_id)

    if todo.user_id != current_user.id:
        abort(403)

    db.session.delete(todo)
    db.session.commit()

    flash('item deleted successfully', 'success')
    return redirect(url_for('list', user_id=current_user.id))


@app.route('/profile/<username>')
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first()
    todos = user.tasks
    todo_list = []
    for todo in todos:
        n_todo = todo.render_todo()
        todo_list.append(n_todo)
    return render_template('profile.html', todos=len(todo_list))




if __name__ == '__main__':
    app.run(debug=True)
