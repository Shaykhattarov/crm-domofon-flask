from app import app, db, login_manager
from flask import render_template, request, flash, redirect, url_for, session
from flask_login import login_required, login_user, logout_user, current_user
from app.models import User, Address
from app.forms import UserLogin, UserRegistration, ClientPaymentForm
from app.forms import OrganizationCreateAddress
from common.authorization import authentication, create_user
from common.address import get_user_address_list, prepare_user_address_list
from common.document import upload_document



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
    address = Address().get_all()
    if form.validate_on_submit():
        result: bool = create_user(name=form.name.data, email=form.email.data, address=form.address.data, phone=form.phone.data)
        if result:
            return redirect(url_for('login'))
        else:
            flash('Произошла ошибка при регистрации. Возможно введены некорректные данные')
            return redirect(url_for('registration'))
    return render_template('/common/registration.html', form=form, address=address)



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
    
    return render_template('/client/tariffs_call.html')



@app.route('/tariffs-call-month', methods=['GET', 'POST'])
def tariffs_call_month():
    if not current_user.is_authenticated: 
        return redirect(url_for('login'))
    
    form = ClientPaymentForm()
    data = {}
    if form.validate_on_submit():
        pass

    return render_template('/client/tariffs_call_pays.html', form=form, data=data)



@app.route('/tariffs-call-year', methods=['GET', 'POST'])
def tariffs_call_year():
    if not current_user.is_authenticated: 
        return redirect(url_for('login'))
    
    form = ClientPaymentForm()
    data = {}
    
    if form.validate_on_submit():
        pass

    return render_template('/client/tariffs_call_pays.html', form=form, data=data)
    


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
    
    return render_template('/operator/pay.html')



@app.route('/operator-report-master', methods=['GET', 'POST'])
def operator_report_master():
    if not current_user.is_authenticated and current_user.role_id != 2:
        return redirect(url_for('login'))

    return render_template('/operator/report-master.html')



@app.route('/operator-tasks-masters', methods=['GET', 'POST'])
def operator_tasks_masters():
    if not current_user.is_authenticated and current_user.role_id != 2:
        return redirect(url_for('login'))
    
    return render_template('/operator/tasks-masters.html')



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



@app.route('/organization-creating-address')
def organization_creating_address():
    if not current_user.is_authenticated and current_user.role_id != 3:
        return redirect(url_for('login'))
    
    form: OrganizationCreateAddress = OrganizationCreateAddress()
    if form.validate_on_submit():
        print('[INFO] Форма создания адреса провалидирована!')

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



@app.route('/organization-code')
def organization_code():
    if not current_user.is_authenticated and current_user.role_id != 3:
        return redirect(url_for('login'))
    
    return render_template('/organization/code.html')






@login_manager.user_loader
def load_user(id):
    return db.session.query(User).get(id)



@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('login'))