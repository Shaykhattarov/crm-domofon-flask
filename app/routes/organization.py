
from app import app
from flask_login import current_user
from flask import request, redirect, url_for, flash, render_template
from app.forms import OrganizationChangeIndividualCode, OrganizationCreateAddress
from common.document import upload_document, view_document
from common.address import save_address, view_addresses, change_address_individual_code


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
            flash('Произошла ошибка! Возможно, неверно введён адрес!')
        else:
            flash('Адреса успешно добавлены!')
            return redirect(url_for('organization_creating_address'))
        
    return render_template('/organization/creating-address.html', form=form)



@app.route('/organization-address')
def organization_address():
    if not current_user.is_authenticated and current_user.role_id != 3:
        return redirect(url_for('login'))

    address_list: list = view_addresses()

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
        address_id = change_address_individual_code(street=form.street.data, district=form.district.data, house=form.house.data, front_door=form.front_door.data, apartment=form.apartment.data, code=form.code.data)
        if address_id is None:
            flash('Ошибка!')
        else:
            flash('Код успешно изменен!')
    return render_template('/organization/code.html', form=form)

