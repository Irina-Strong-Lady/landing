from flask import render_template, request, redirect, url_for, flash
from . import main
from .. import db
from .. models import User, Claim
from . forms import ClaimEditForm

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
            message = f'Мы рады снова видеть Вас {email}! Специалист свяжется с Вами в ближайшее время!'
            return render_template('index.html', repeat=message)
        message = f'Специалист свяжется с Вами по адресу {email} в ближайшее время!'
        return render_template('index.html', success=message)
    return redirect(url_for('main.index'))

@main.route('/claim', methods=['GET', 'POST'])
def claim_form():
    form = ClaimEditForm()
    user = User()
    if form.validate_on_submit():
        user.name = form.name.data
        user.email = form.email.data
        user.phone_number = form.phone_number.data        
        db.session.add(user)
        db.session.flush()
        claim = Claim(user)
        claim.fabula = form.fabula.data                
        db.session.add(claim)
        db.session.commit()
        if isinstance(form.name.data, str) and form.name.data[-1] in ['а', 'a']:
            message = f'Уважаемая {form.name.data}! Заявка принята. Ответ поступит на {form.email.data} или {form.phone_number.data}'
        else:
            message = f'Уважаемый {form.name.data}! Заявка принята. Ответ поступит на {form.email.data} или {form.phone_number.data}'
        return render_template('index.html', success=message)
    return render_template('claimform.html', form=form)
    