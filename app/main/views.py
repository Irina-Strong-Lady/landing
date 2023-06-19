from flask import render_template, request, redirect, url_for
from . import main
from .. import db
from .. models import User

@main.route('/')
def index():    
    return render_template('index.html')

@main.route('/email', methods=['GET', 'POST'])
def get_email():
    user = User()   
    if request.method == 'POST' and request.form.get('email') != '':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        if not user:
            user = User()
            setattr(user, 'email', email)
            db.session.add(user)
            db.session.commit()
        else:
            message = f'Мы рады снова видеть Вас {email}! Oтвет будет направлен в ближайшее время!'
            return render_template('index.html', repeat=message)
        message = f'Ответ на адрес {email} будет направлен в ближайшее время!'
        return render_template('index.html', success=message)
    return redirect(url_for('main.index'))
    