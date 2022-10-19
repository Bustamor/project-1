from flask_app.models.user_model import User
from flask_app import app, render_template, redirect, request, session, flash, bcrypt

#redirect user to login_reg
@app.route('/')
def redirect_user():
    return redirect('/users/login_reg')

@app.get('/users/login_reg')
def login_reg():
    return render_template('login_reg.html')

@app.post('/users/register')
def register_user():
    # check if form is valid
    if not User.validate_registration(request.form):
        return redirect('/users/login_reg')
    
    # if form is valid, check to see if already reg
    found_user = User.find_by_email(request.form)
    if found_user:
        flash('Email already in database. Please login', 'email')
        return redirect('/users/login_reg')

    # # passsword (encrypt w bcrypt)
    hashed = bcrypt.generate_password_hash(request.form['password'])

    # print(hashed)
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': hashed
    }

    # register (save) the user
    user_id = User.save(data)

    #log user in and save user's id in session
    session['user_id'] = user_id
    return redirect('/habits')

@app.post('/users/login')
def login_user():
    # validate  if form is valid
    if not User.validate_login(request.form):
        return redirect('/users/login_reg')

    # if form is valid, check to see if they are registered
    found_user = User.find_by_email(request.form)
    if not found_user:
        flash('Email not found, please register', 'log_email')
        return redirect('/users/login_reg')
    # if they did register, check pw crrect
    if not bcrypt.check_password_hash(found_user.password, request.form['password']):
        flash('Invalid credential. Please check your password', 'log_password')
        return redirect('/users/login_reg')
    # log them in
    session['user_id'] = found_user.id
    return redirect('/habits')
    
@app.get('/habits')
def habits():
    if 'user_id' not in session:
        return redirect('/users/login_reg')
    data = {
        'id': session['user_id']
    }
    user = User.find_by_id(data)
    return render_template('habits.html', user = user)

@app.get('/users/logout')
def logout():
    session.clear()
    return redirect('/users/login_reg')
    

