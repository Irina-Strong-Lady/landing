import os
from flask import render_template, request, redirect, url_for, flash
from . import main
from .. import db
from .. models import User, Claim
from . forms import ClaimEditForm
from app.email import send_email

@main.route('/')
def index():    
    return render_template('index.html')

@main.route('/email', methods=['GET', 'POST'])
def get_email():
    if request.method == 'POST' and request.form.get('email') != '':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        if not user:
            user = User(email=email)
            db.session.add(user)
            db.session.commit()
            message = f'Специалист свяжется с Вами по адресу {user.email}!'
            send_email(os.environ.get('APP_ADMIN'), f'Обращение без заявки от клиента {user.email}', 'mail/email_only_admin', user=user)
            send_email(user.email, f'Ответ специалиста придет на {user.email} ', 'mail/email_only_user', user=user)
        else:
            message = f'Мы рады снова видеть Вас {user.email}! Специалист свяжется с Вами!'
            send_email(os.environ.get('APP_ADMIN'), f'Обращение без заявки от клиента {user.email}', 'mail/email_only_admin', user=user)
            send_email(user.email, f'Ответ специалиста придет на {user.email} ', 'mail/email_only_user', user=user)
            return render_template('index.html', repeat=message)
        return render_template('index.html', success=message)
    return redirect(url_for('main.index'))

@main.route('/claim', methods=['GET', 'POST'])
def claim_form():
    form = ClaimEditForm()
    user = User()
    if form.validate_on_submit():
        user = User(name=form.name.data,
                    email = form.email.data,
                    phone_number = form.phone_number.data
                    )
        db.session.add(user)
        db.session.flush()
        claim = Claim(user)
        claim.fabula = form.fabula.data
        db.session.add(claim)
        db.session.commit()
        send_email(os.environ.get('APP_ADMIN'), f'Заявка № {claim.id}', 'mail/send_admin', user=user, claim=claim)
        send_email(user.email, f'Номер Вашей заявки (заявка № {claim.id})', 'mail/send_user', user=user, claim=claim)
        if isinstance(form.name.data, str) and form.name.data[-1] in ['а', 'a']:
            message = f'Уважаемая {form.name.data}! Заявка принята. Ответ поступит на {form.email.data} или {form.phone_number.data}'
        else:
            message = f'Уважаемый {form.name.data}! Заявка принята. Ответ поступит на {form.email.data} или {form.phone_number.data}'        
        return render_template('claimform.html', form=form, success=message)
    return render_template('claimform.html', form=form)
    