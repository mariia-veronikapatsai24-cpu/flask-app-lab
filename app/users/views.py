from flask import Blueprint, render_template, request, redirect, url_for, session, flash

users_bp = Blueprint('users', __name__, template_folder='templates')

VALID_USERNAME = 'user1'
VALID_PASSWORD = 'password123'

@users_bp.route('/hi/<string:name>')
def greetings(name):
    name = name.upper()
    age = request.args.get('age', None, int)
    return render_template('users/hi.html', name=name, age=age)

@users_bp.route('/admin')
def admin():
    to_url = url_for('users.greetings', name='administrator', age=45, _external=True)
    return redirect(to_url)

@users_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == VALID_USERNAME and password == VALID_PASSWORD:
            session['username'] = username
            flash('Успішний вхід!', 'success')
            return redirect(url_for('users.profile'))
        else:
            flash('Невірні дані! Спробуйте ще раз.', 'danger')
    return render_template('users/login.html')

@users_bp.route('/profile')
def profile():
    if 'username' not in session:
        flash('Будь ласка, увійдіть спочатку.', 'warning')
        return redirect(url_for('users.login'))
    theme = request.cookies.get('theme', 'light')
    return render_template('users/profile.html', username=session['username'], theme=theme)

@users_bp.route('/logout')
def logout():
    session.pop('username', None)
    flash('Ви вийшли з системи.', 'info')
    return redirect(url_for('users.login'))

@users_bp.route('/set_cookie', methods=['POST'])
def set_cookie():
    if 'username' not in session:
        return redirect(url_for('users.login'))
    key = request.form.get('key')
    value = request.form.get('value')
    max_age = request.form.get('max_age', 3600, type=int)
    response = redirect(url_for('users.profile'))
    response.set_cookie(key, value, max_age=max_age)
    flash(f'Кукі "{key}" додано!', 'success')
    return response

@users_bp.route('/delete_cookie', methods=['POST'])
def delete_cookie():
    if 'username' not in session:
        return redirect(url_for('users.login'))
    key = request.form.get('key')
    response = redirect(url_for('users.profile'))
    response.delete_cookie(key)
    flash(f'Кукі "{key}" видалено!', 'success')
    return response

@users_bp.route('/delete_all_cookies', methods=['POST'])
def delete_all_cookies():
    if 'username' not in session:
        return redirect(url_for('users.login'))
    response = redirect(url_for('users.profile'))
    for key in request.cookies:
        response.delete_cookie(key)
    flash('Всі кукі видалено!', 'success')
    return response

@users_bp.route('/set_theme/<theme>')
def set_theme(theme):
    if theme not in ['light', 'dark']:
        theme = 'light'
    response = redirect(url_for('users.profile'))
    response.set_cookie('theme', theme, max_age=30*24*3600)
    return response