from flask import render_template, request
from . import main
from .. import db
from .. models import User

@main.route('/')
def index():    
    return render_template('index.html')

@main.route('/404')
def error_404():
    return render_template('404.html')

@main.route('/email', methods=['GET', 'POST'])
def get_email():
    user = User()   
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        if not user:
            user = User()
            setattr(user, 'email', email)
            db.session.add(user)
            db.session.commit()
        else:
            message = f'Пользователь с адресом {email} уже существует'
            return render_template('index.html', error=message)
        message = f'Пользователь с адресом {email} зарегистрирован'
    return render_template('index.html', success=message)
    