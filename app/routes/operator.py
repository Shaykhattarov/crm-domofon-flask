import math, json
from app import app
from flask import redirect, url_for, flash, request, render_template
from flask_login import login_required, current_user
from app.forms import CreateApplicationForm, OperatorPay, CreateMasterReportForm
from app.forms import ViewReportApplicationForm, ViewReportMasterForm, ChangeApplicationForm
from common.address import generate_address_hints
from common.payment import operator_pay_lk
from common.report import create_report, view_report_about_master, view_report_about_applications, view_report_about_payments
from common.application import count_application, create_application, change_application



@app.route('/operator-create-order', methods=['GET', 'POST'])
@login_required
def operator_create_order():
    if not current_user.is_authenticated and current_user.role_id != 2:
        return redirect(url_for('login'))
    
    data = {}
    hints = generate_address_hints()
    form: CreateApplicationForm = CreateApplicationForm()
    form.add_master_choices()
    form.add_district_choices()
    data['id']: int = count_application() + 1
    if form.validate_on_submit():
        result = create_application(district_id=form.district.data, street=form.street.data, front_door=form.front_door.data, house=form.house.data, apartment=form.apartment.data, 
                                    master_id=form.master.data, date=form.date.data, problem=form.problem.data, image=form.image.data)
        if result['error'] == '':
            flash('Заявка успешно создана!')
            return redirect(url_for('operator_create_order'))
        else:
            flash('Произошла ошибка при создании заявки или данный адрес не существует!')
            return redirect(url_for('operator_create_order'))
        
    return render_template('/operator/create-order.html', form=form, data=data, hints=hints)


@app.route('/operator-pay', methods=['GET', 'POST'])
def operator_pay():
    if not current_user.is_authenticated and current_user.role_id != 2:
        return redirect(url_for('login'))
    
    hints = generate_address_hints()
    form: OperatorPay = OperatorPay()
    form.add_tariff_choices()
    form.add_district_choices()
    if form.validate_on_submit():
        amount = float(form.amount.data)
        if amount <= 0:
            flash("Введена некорректная сумма")
            return redirect(url_for('operator_pay'))
        else:
            amount: int = math.ceil(amount)
    
        pay: dict = operator_pay_lk(district_id=form.district.data, street=form.street.data, front_door=form.front_door.data, house=form.house.data, apartment=form.apartment.data,
                                     amount=amount, tariff_id=form.tariff.data)
        if pay['status'] == 'good':
            flash("Оплата проведена успешно!")
        else:
            flash(pay['message'])
    
    return render_template('/operator/pay.html', form=form, hints=hints)

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
    hints = generate_address_hints()
    form = ViewReportApplicationForm()
    form.add_district_choices()
    if form.validate_on_submit():
        result = view_report_about_payments(district_id=form.district.data, street=form.street.data, house=form.house.data, front_door=form.front_door.data, 
                                            apartment=form.apartment.data, from_date=form.from_date.data, to_date=form.to_date.data)
        if result['error'] is None or result['error'] == '':
            flash(result['message'][0], 'debt')
            flash(result['message'][1], 'option')
            flash(result['message'][2], 'tariff')
            return redirect(url_for('operator_report_pays'))
        else:
            flash(result['message'], 'error')
            return redirect(url_for('operator_report_pays'))

    return render_template('/operator/report-pays.html', form=form, data=data, hints=hints)


@app.route('/operator-report-request', methods=['GET', 'POST'])
def operator_report_request():
    if not current_user.is_authenticated and current_user.role_id != 2:
        return redirect(url_for('login'))
    
    data = {}
    hints = generate_address_hints()
    form = ViewReportApplicationForm()
    form.add_district_choices()
    if form.validate_on_submit():
        result = view_report_about_applications(district_id=form.district.data, street=form.street.data, house=form.house.data, front_door=form.front_door.data, 
                                                apartment=form.apartment.data, from_date=form.from_date.data, to_date=form.to_date.data)
        if result['error'] == '':
            flash(result['message'][0],'applications_count')
            flash(result['message'][1], 'return_applications')
            return redirect(url_for('operator_report_request'))
        else:
            flash(result['message'],'applications_count')
            flash(result['message'], 'return_applications')
            return redirect(url_for('operator_report_request'))
    
    return render_template('/operator/report-request.html', form=form, data=data, hints=hints)


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

