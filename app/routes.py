import json
import math
from app import app, db, login_manager
from flask import render_template, request, flash, redirect, url_for, session
from flask_login import login_required, login_user, logout_user, current_user
from app.models import User, Tariff
from app.forms import UserLogin, UserRegistration
from app.forms import OrganizationCreateAddress, OrganizationChangeIndividualCode
from app.forms import OperatorPay
from common.authorization import authentication, create_user
from common.address import get_user_address_list, prepare_user_address_list, save_address, change_address_individual_code, generate_address_help_list, generate_apartment_help_list
from common.document import upload_document
from common.payment import operator_pay_lk, equiring



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



@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    
    form = UserRegistration()
    options = generate_address_help_list()
    if form.validate_on_submit():
        result: bool = create_user(name=form.name.data, email=form.email.data, address=form.address.data, phone=form.phone.data)
        if result['status'] == 'good':
            return redirect(url_for('login'))
        else:
            flash(result['message'])
    return render_template('/common/registration.html', form=form, options=options)



@app.route('/profile')
@login_required
def profile():
    if not current_user.is_authenticated: 
        return redirect(url_for('login'))
    
    role_id = int(session.get('role_id'))

    match role_id:
        case 1:
            return render_template('/client/profile.html')
        case 2:
            return render_template('/operator/profile.html')
        case 3:
            return render_template('/organization/profile.html')
        case 4:
            return render_template('/master/profile.html')
        case _:
            return redirect(url_for('login'))



@app.route('/tariffs', methods=['GET', 'POST'])
@login_required
def client_tariffs():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    if request.method == 'POST':
       checkbox = request.form.get('agreement')
       if checkbox is None:
           flash('Пожалуйста, примите соглашение об оферте!')
           return redirect(url_for('client_tariffs'))
           
       phone = request.form.get('phone')
       notphone = request.form.get('notphone')
       if phone is not None:
           session['phone'] = True
           return redirect(url_for('tariffs_call'))
       
       if notphone is not None:
           session['phone'] = False
           return redirect(url_for('tariffs_call'))
       
    return render_template('/client/tariffs.html')



@app.route('/contract-offer')
@login_required
def contract_offer():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    
    return render_template('/client/contract_offer.html')



@app.route('/payments')
@login_required
def client_payments():
    if not current_user.is_authenticated: 
        return redirect(url_for('login'))
    
    return render_template('/client/payments.html')
    


@app.route('/tariffs-call')
@login_required
def tariffs_call():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    
    if session['phone']:
        tariff = db.session.query(Tariff).get(1)
    else:
        tariff = db.session.query(Tariff).get(2)

    session['month'] = tariff.price
    session['year'] = tariff.price * 12
    
    return render_template('/client/tariffs_call.html', month=tariff.price, year=(tariff.price * 12))



@app.route('/tariffs-call-month', methods=['GET', 'POST'])
def tariffs_call_month():
    if not current_user.is_authenticated: 
        return redirect(url_for('login'))
    
    equiring(user_id=current_user.id, amount=session['month'])

    return 'Привет', 200




@app.route('/tariffs-call-year', methods=['GET', 'POST'])
def tariffs_call_year():
    if not current_user.is_authenticated: 
        return redirect(url_for('login'))
    
    


@app.route('/operator-create-order', methods=['GET', 'POST'])
@login_required
def operator_create_order():
    if not current_user.is_authenticated and current_user.role_id != 2:
        return redirect(url_for('login'))
    
    return render_template('/operator/create-order.html')



@app.route('/operator-pay', methods=['GET', 'POST'])
def operator_pay():
    if not current_user.is_authenticated and current_user.role_id != 2:
        return redirect(url_for('login'))
    
    form: OperatorPay = OperatorPay()
    address_list: list = generate_address_help_list()
    if form.validate_on_submit():
        amount = float(form.amount.data)
        if amount <= 0:
            flash("Введена некорректная сумма")
            return redirect(url_for('operator_pay'))
        else:
            amount: int = math.ceil(amount)

        pay: dict = operator_pay_lk(address=form.address.data, apartment=form.apartment.data, amount=amount)

        if pay['status'] == 'good':
            flash("Оплата проведена успешно!")
        else:
            flash(pay['message'])
    
    return render_template('/operator/pay.html', form=form, address_list=address_list)

@app.route('/operator-pay/apartment/', methods=['POST'])
def operator_pay_get_apartment():
    address: str = request.get_data(as_text=True)
    data: list = generate_apartment_help_list(address=address)
    if data is not None:
        return json.dumps(data)
    else:
        return 'Empty message', 404



@app.route('/operator-report-master', methods=['GET', 'POST'])
def operator_report_master():
    if not current_user.is_authenticated and current_user.role_id != 2:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        app_id = request.form.get('number')
        status = request.form.get('status')
        master = request.form.get('master')

    return render_template('/operator/report-master.html')



@app.route('/operator-tasks-masters', methods=['GET', 'POST'])
def operator_tasks_masters():
    if not current_user.is_authenticated and current_user.role_id != 2:
        return redirect(url_for('login'))
    
    return render_template('/operator/tasks-masters.html')



@app.route('/operator-report-masters', methods=['GET', 'POST'])
def operator_report_masters():
    if not current_user.is_authenticated and current_user.role_id != 2:
        return redirect(url_for('login'))
    
    return render_template('/operator/report-masters.html')



@app.route('/operator-report-pays', methods=['GET', 'POST'])
def operator_report_pays():
    if not current_user.is_authenticated and current_user.role_id != 2:
        return redirect(url_for('login'))

    return render_template('/operator/report-pays.html')



@app.route('/operator-list-masters')
def operator_list_masters():
    if not current_user.is_authenticated and current_user.role_id != 2:
        return redirect(url_for('login'))
    
    return render_template('/operator/list-masters.html')



@app.route('/operator-report-request')
def operator_report_request():
    if not current_user.is_authenticated and current_user.role_id != 2:
        return redirect(url_for('login'))
    
    return render_template('/operator/report-request.html')



@app.route('/operator-edit')
def operator_edit():
    if not current_user.is_authenticated and current_user.role_id != 2:
        return redirect(url_for('login'))
    
    return render_template('/operator/edit.html')



@app.route('/organization-creating-address', methods=['GET', 'POST'])
def organization_creating_address():
    if not current_user.is_authenticated and current_user.role_id != 3:
        return redirect(url_for('login'))
    
    form: OrganizationCreateAddress = OrganizationCreateAddress()
    form.add_equipment_choices()
    form.add_tariff_choices()
    if form.validate_on_submit():
        print('[INFO] Форма создания адреса провалидирована!')
        address_id = save_address(street=form.street.data, house=form.house.data, front_door=form.front_door.data, tariff_id=form.tariff.data, equipment_list_id=form.equipment.data, serial_code=form.serial_code.data)
        print(address_id)
    return render_template('/organization/creating-address.html', form=form)



@app.route('/organization-address')
def organization_address():
    if not current_user.is_authenticated and current_user.role_id != 3:
        return redirect(url_for('login'))

    address_list: list = get_user_address_list()
    address_list: list = prepare_user_address_list(address_list=address_list)

    return render_template('/organization/address.html', address_list=address_list)



@app.route('/organization-master-reports')
def organization_master_reports():
    if not current_user.is_authenticated and current_user.role_id != 3:
        return redirect(url_for('login'))
    
    return render_template('/organization/master-reports.html')



@app.route('/organization-report')
def organization_report(id=None):
    if not current_user.is_authenticated and current_user.role_id != 3:
        return redirect(url_for('login'))
    
    master_id = request.args.get('id')
    print(master_id)
    
    return render_template('/organization/report.html')



@app.route('/organization-docs', methods=['GET', 'POST'])
def organization_docs():
    if not current_user.is_authenticated and current_user.role_id != 3:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        file = request.files.get('document')
        if file.filename is not None and file.filename != '':
            filepath: str = upload_document(file=file)
            flash("Документ успешно сохранен!")
        else:
            flash("Документ не был выбран! Или произошла ошибка в время передачи файла!")

    return render_template('/organization/docs.html')



@app.route('/organization-code', methods=['GET', 'POST'])
def organization_code():
    if not current_user.is_authenticated and current_user.role_id != 3:
        return redirect(url_for('login'))
    
    form: OrganizationChangeIndividualCode = OrganizationChangeIndividualCode()
    help_list = generate_address_help_list()
    if form.validate_on_submit():
        print(form.code.data)
        address_id = change_address_individual_code(address=form.address.data, code=form.code.data)
        print(address_id)
    return render_template('/organization/code.html', form=form, datalist=help_list)





@login_manager.user_loader
def load_user(id):
    return db.session.query(User).get(id)



@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('login'))