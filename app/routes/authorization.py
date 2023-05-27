from app import app, db, login_manager
from app.models import User
from app.forms import UserLogin, UserRegistration

from flask import render_template, flash, redirect, url_for, session
from flask_login import login_required, login_user, logout_user, current_user

from common.authorization import authentication, create_user
from common.address import get_individual_code, generate_address_hints
from common.payment import check_subscriptions



@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))

    form = UserLogin()
    if form.validate_on_submit():
        result: dict = authentication(name=form.name.data, email=form.email.data)
        if result['status']:
            user: list = result['result']
            login_user(user)
            session['role_id'] = user.role_id
            match user.role_id:
                case 1:
                    return redirect(url_for('profile'))
                case 2:
                    return redirect(url_for('profile'))
                case 3:
                    return redirect(url_for('profile'))
                case 4:
                    return redirect(url_for('profile'))
        else:
            if result['result'] is not None:
                flash('Произошла ошибка авторизации')
            else:
                flash('Неправильное имя или email')
            return redirect(url_for('login'))
    return render_template('/common/login.html', form=form)


@app.route('/reg', methods=['GET', 'POST'])
@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    
    hints = generate_address_hints()
    form = UserRegistration()
    form.add_district_choices() # Добавление выбора районов
    if form.validate_on_submit():
        if form.district.data == 0:
            flash('Выберите район')
            return redirect('registration')
        
        result: bool = create_user(name=form.name.data, email=form.email.data, phone=form.phone.data, street=form.street.data, district=form.district.data, house=form.house.data, 
                                   front_door=form.front_door.data, apartment=form.apartment.data)
        
        if result['status'] == 'good':
            return redirect(url_for('login'))
        else:
            flash(result['message'])
            
    return render_template('/common/registration.html', form=form, hints=hints)


@app.route('/profile')
@login_required
def profile():
    if not current_user.is_authenticated: 
        return redirect(url_for('login'))
    
    role_id = int(session.get('role_id'))

    match role_id:
        case 1:
            check_subscriptions()
            individual_code = get_individual_code(user_id=current_user.id)
            return render_template('/client/profile.html', individual_code=individual_code)
        case 2:
            #check_subscriptions() # Проверка и удаление подписки по истечению срока
            return render_template('/operator/profile.html')
        case 3:
            #check_subscriptions() # Проверка и удаление подписки по истечению срока
            return render_template('/organization/profile.html')
        case 4:
            return render_template('/master/profile.html')
        case _:
            return redirect(url_for('login'))


@login_manager.user_loader
def load_user(id):
    return db.session.query(User).get(id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('login'))