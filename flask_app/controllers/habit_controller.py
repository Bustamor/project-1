from pprint import pprint
from flask_app import app, render_template, redirect, request, session
from flask_app.models.user_model import User
from flask_app.models.habit_model import Habit

# display all habits
@app.get('/habits')
def all_habits():
    if 'user_id' not in session:
        return redirect('/users/login_reg')
    data = {
        'id': session['user_id']
    }
    user = User.find_by_id(data)
    habits = Habit.find_all()
    return render_template('habits.html', user = user, habits = habits)

# display form to create habit
@app.get('/habits/new')
def new_habit():
    if 'user_id' not in session:
        return redirect('/users/login_reg')
    return render_template('new_habit.html')

# process form and create habit
@app.post('/habits')
def create_habit():
    pprint ("************************ IN CREATE HABIT")
    if not Habit.validate_habit(request.form):
        return redirect('/habits/new')
    Habit.save(request.form)
    return redirect('/habits')

# display one habit
@app.get('/habits/<int:habit_id>')
def one_habit(habit_id):
    if 'user_id' not in session:
        return redirect('/users/login_reg')
    data = {
        'id': habit_id
    }
    habit = Habit.find_by_id_with_creator(data)
    return render_template('one_habit.html', habit = habit)

# display form to edit habit
@app.get('/habits/<int:habit_id>/edit')
def edit_habit(habit_id):
    if 'user_id' not in session:
        return redirect('/users/login_reg')
    data = {
        'id': habit_id
    }
    habit = Habit.find_by_id_with_creator(data)
    return render_template('edit_habit.html', habit = habit)

@app.post('/habits/<int:habit_id>/update')
def update_habit(habit_id):
    
    if not Habit.validate_habit(request.form):
        return redirect(f'/habits/{habit_id}/edit')
    Habit.find_by_id_and_update(request.form)
    return redirect(f'/habits/{habit_id}')

@app.get('/habits/<int:habit_id>/delete')
def delete_habit(habit_id):
    if 'user_id' not in session:
        return redirect('/users/login_reg')
    data = {
        'id': habit_id
    }
    Habit.find_by_id_and_delete(data)
    return redirect('/habits')