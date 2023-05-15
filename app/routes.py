import json, math
from app import app, db, login_manager
from flask import render_template, request, flash, redirect, url_for, session
from flask_login import login_required, login_user, logout_user, current_user
from app.models import User, Tariff
from app.forms import UserLogin, UserRegistration
from app.forms import OrganizationCreateAddress, OrganizationChangeIndividualCode
from app.forms import OperatorPay, CreateApplicationForm, ChangeApplicationForm, CreateMasterReportForm, ViewReportMasterForm, ViewReportApplicationForm
from common.authorization import authentication, create_user
from common.address import get_user_address_list, prepare_user_address_list, save_address, change_address_individual_code, generate_apartment_help_list, get_individual_code
from common.document import upload_document, view_document
from common.payment import operator_pay_lk, equiring, successfull_payment, get_payments, check_subscriptions
from common.application import count_application, create_application, change_application
from common.report import create_report, view_report_about_master, view_report_about_applications, view_report_about_payments
from common import generate_address_help_list, generate_houses_help_list, generate_streets_help_list



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
    
    form = UserRegistration()
    options= generate_address_help_list()
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
            
    return render_template('/common/registration.html', form=form, options=options)


@app.route('/ajax/registration/district', methods=['GET'])
def ajax_registration_support_by_district():
    district_id = request.args.get('district_id')
    if district_id is None:
        return 400
    streets = generate_streets_help_list()
    return json.dumps(streets)


@app.route('/ajax/registration/street', methods=['GET'])
def ajax_registration_support_by_street():
    street = request.args.get('street')
    if street is None:
        return 400
    houses = generate_houses_help_list(street=street)
    return json.dumps(houses)



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
    
    payments = []
    payments: list[dict] = get_payments(user_id=current_user.id)
    
    return render_template('/client/payments.html', payments=payments)
    


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

    response = equiring(user_id=current_user.id, amount=session['month'])
    if response is None or response['error'] == '':
        return redirect(response['payment_url'])
    else:
        if response['message'] is not None:
            flash(response['message'])
            return redirect(url_for('tariff-calls'))
        else:
            flash('Ошибка оплаты')
            return redirect(url_for('tariff-calls'))



@app.route('/successfull-payment', methods=['GET', 'POST'])
def success_payment():
    response = successfull_payment(request)
    if response['error'] == '':
        return redirect(url_for('profile'))
    else:
        return redirect(url_for('error_payment'))
    


@app.route('/error-payment', methods=['GET', 'POST'])
def error_payment():
    return "Ошибка оплаты"



@app.route('/tariffs-call-year', methods=['GET', 'POST'])
def tariffs_call_year():
    if not current_user.is_authenticated: 
        return redirect(url_for('login'))
    
    response = equiring(user_id=current_user.id, amount=session['year'])
    if response['error'] == '':
        return redirect(response['payment_url'])
    else:
        if response['message'] is not None:
            flash(response['message'])
            return redirect(url_for('tariff-calls'))
        else:
            flash('Ошибка оплаты')
            return redirect(url_for('tariff-calls'))



@app.route('/operator-create-order', methods=['GET', 'POST'])
@login_required
def operator_create_order():
    if not current_user.is_authenticated and current_user.role_id != 2:
        return redirect(url_for('login'))
    
    data = {}
    form: CreateApplicationForm = CreateApplicationForm()
    form.add_master_choices()
    data['id']: int = count_application() + 1
    data['address'] = generate_address_help_list()
    if form.validate_on_submit():
        result = create_application(address=form.address.data, apartment=form.apartment.data, master_id=form.master.data, problem=form.problem.data, date=form.date.data, image=form.image.data)
        if result['error'] == '':
            flash("Заявка успешно создана!")
        else:
            flash("Произошла ошибка!")

    return render_template('/operator/create-order.html', form=form, data=data)



@app.route('/operator-pay', methods=['GET', 'POST'])
def operator_pay():
    if not current_user.is_authenticated and current_user.role_id != 2:
        return redirect(url_for('login'))
    
    form: OperatorPay = OperatorPay()
    form.add_tariff_choices()
    address_list: list = generate_address_help_list()
    if form.validate_on_submit():
        amount = float(form.amount.data)
        if amount <= 0:
            flash("Введена некорректная сумма")
            return redirect(url_for('operator_pay'))
        else:
            amount: int = math.ceil(amount)
    
        pay: dict = operator_pay_lk(address=form.address.data, apartment=form.apartment.data, amount=amount, tariff_id=form.tariff.data)

        if pay['status'] == 'good':
            flash("Оплата проведена успешно!")
        else:
            flash(pay['message'])
    
    return render_template('/operator/pay.html', form=form, address_list=address_list)

@app.route('/operator/apartment/', methods=['POST'])
def operator_get_apartment():
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
    
    form = CreateMasterReportForm()
    form.add_application_choices()
    form.add_status_choices()
    form.add_master_choices()
    if form.validate_on_submit():
        result = create_report(app_id=form.number.data, status_id=form.status.data, master_id=form.master.data, addition=form.addition.data, image=form.image.data, date=form.date.data)
        flash('Отчет успешно сохранен!')
        return redirect(url_for('operator_report_master'))
    return render_template('/operator/report-master.html', form=form)



@app.route('/operator-report-masters', methods=['GET', 'POST'])
def operator_report_masters():
    if not current_user.is_authenticated and current_user.role_id != 2:
        return redirect(url_for('login'))
    
    form = ViewReportMasterForm()
    form.add_master_choices()
    if form.validate_on_submit():
        result = view_report_about_master(master_id=form.master.data, from_date=form.from_date.data, to_date=form.to_date.data)
        flash(result[0],'applications_count')
        flash(result[1], 'return_applications')
        return redirect(url_for('operator_report_masters'))
    return render_template('/operator/report-masters.html', form=form)



@app.route('/operator-report-pays', methods=['GET', 'POST'])
def operator_report_pays():
    if not current_user.is_authenticated and current_user.role_id != 2:
        return redirect(url_for('login'))
    
    data = {}
    form = ViewReportApplicationForm()
    data['address'] = generate_address_help_list()
    if form.validate_on_submit():
        result = view_report_about_payments(address=form.address.data, appartment=form.apartment.data, from_date=form.from_date.data, to_date=form.to_date.data)
        if result['error'] is None or result['error'] == '':
            flash(result['message'][0], 'debt')
            flash(result['message'][1], 'option')
            flash(result['message'][2], 'tariff')
            return redirect(url_for('operator_report_pays'))
        else:
            flash(result['message'], 'error')
            return redirect(url_for('operator_report_pays'))

    return render_template('/operator/report-pays.html', form=form, data=data)



@app.route('/operator-report-request', methods=['GET', 'POST'])
def operator_report_request():
    if not current_user.is_authenticated and current_user.role_id != 2:
        return redirect(url_for('login'))
    
    data = {}
    form = ViewReportApplicationForm()
    data['address'] = generate_address_help_list()
    if form.validate_on_submit():
        result = view_report_about_applications(address=form.address.data, apartment=form.apartment.data, from_date=form.from_date.data, to_date=form.to_date.data)
        flash(result[0],'applications_count')
        flash(result[1], 'return_applications')
    
    return render_template('/operator/report-request.html', form=form, data=data)



@app.route('/operator-edit-order', methods=['GET', 'POST'])
def operator_edit():
    if not current_user.is_authenticated and current_user.role_id != 2:
        return redirect(url_for('login'))
    
    form = ChangeApplicationForm()
    form.add_application_choices()
    form.add_status_choices()
    if form.validate_on_submit():
        change_application(num=form.number.data, problem=form.problem.data, date=form.date.data, status_id=form.status.data, image=form.image.data)
        flash('Заявка успешно изменена!')
        return redirect(url_for('operator_edit'))

    return render_template('/operator/edit.html', form=form)



@app.route('/organization-creating-address', methods=['GET', 'POST'])
def organization_creating_address():
    if not current_user.is_authenticated and current_user.role_id != 3:
        return redirect(url_for('login'))
    
    form: OrganizationCreateAddress = OrganizationCreateAddress()
    form.add_equipment_choices()
    form.add_tariff_choices()
    form.add_district_choices()
    if form.validate_on_submit():
        if form.district.data == 0:
            flash('Выберите район!')
            return redirect(url_for('organization_creating_address'))
        address_id = save_address(street=form.street.data, house=form.house.data, front_door=form.front_door.data, apartment_from=int(form.from_apartment.data), apartment_to=int(form.to_apartment.data), 
                                  tariff_id=form.tariff.data, equipment_list_id=form.equipment.data, district_id=form.district.data, serial_code=form.serial_code.data)
        if not address_id:
            flash('Произошла ошибка!')
        else:
            flash('Адреса успешно добавлены!')
            return redirect(url_for('organization_creating_address'))
        
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



@app.route('/organization-view-docs', methods=['GET', 'POST'])
def organization_view_docs():
    if not current_user.is_authenticated and current_user.role_id != 3:
        return redirect(url_for('login'))
    
    filelist = view_document()
    if filelist['status']:
        return render_template('/organization/view-docs.html', filelist=filelist['message'])
    else:
        return render_template('/organization/view-docs.html', filelist=False)



@app.route('/organization-code', methods=['GET', 'POST'])
def organization_code():
    if not current_user.is_authenticated and current_user.role_id != 3:
        return redirect(url_for('login'))
    
    form: OrganizationChangeIndividualCode = OrganizationChangeIndividualCode()
    form.add_district_choices()
    if form.validate_on_submit():
        address_id = change_address_individual_code(street=form.street.data, district=form.district.data, house=form.house.data, front_door=form.front_door, apartment=form.apartment.data, code=form.code.data)
    return render_template('/organization/code.html', form=form)




@login_manager.user_loader
def load_user(id):
    return db.session.query(User).get(id)



@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('login'))