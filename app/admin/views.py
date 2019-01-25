from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from . import admin
from .forms import DepartmentForm, RoleForm, EmployeeAssignForm
from .. import db
from ..models import Department, Role, Employee


def check_admin():
    """
    Prevent non-admins from accessing the page
    """
    if not current_user.is_admin:
        abort(403)


@login_required
@admin.route('/departments', methods=['GET', 'POST'])
def list_departments():
    """
    List all departments
    """
    check_admin()

    departments = Department.query.all()

    return render_template('admin/departments/departments.html',
                            departments=departments, title="Departments")


@login_required
@admin.route('/departments/add', methods=['GET', 'POST'])
def add_department():
    """
    Add a department to the database
    """
    check_admin()

    add_department = True

    form = DepartmentForm()
    if form.validate_on_submit():
        department = Department(name=form.name.data,
                                description=form.description.data)
        try:
            # add department to the database
            db.session.add(department)
            db.session.commit()
            flash('You have successfully added a new department')
        except:
            # in case department name already exists
            flash('Error: department name already exists')

        # redirect to department page
        return redirect(url_for('admin.list_departments'))

    # load department template
    return render_template('admin/departments/department.html', action="Add",
                            add_department=add_department, form=form,
                            title="Add Department")


@login_required
@admin.route('/department/edit/<int:id>', methods=['GET', 'POST'])
def edit_department(id):
    """
    Edit a department
    """
    check_admin()

    add_department = False

    department = Department.query.get_or_404(id)
    form = DepartmentForm(obj=department)
    if form.validate_on_submit():
        department.name = form.name.data
        department.description = form.description.data
        db.session.commit()
        flash('You have successfully edited the department')

        # redirect to the department page
        return redirect(url_for('admin.list_departments'))

    form.description.data = department.description
    form.name.data = department.name
    return render_template('admin/departments/department.html', action="Edit",
                            add_department=add_department, form=form,
                            department=department, title="Edit Department")


@login_required
@admin.route('/departments/delete/<int:id>', methods=['GET', 'POST'])                            
def delete_department(id):
    """
    Delete a department from the database
    """
    check_admin()

    department = Department.query.get_or_404(id)
    if department is not None:
        db.session.delete(department)
        db.session.commit()
        flash('You have successfully deleted  the department.')

        # redirect to the departments page
        return redirect(url_for('admin.list_departments'))

    return render_template(title="Delete Department")


@login_required
@admin.route('/roles')
def list_roles():
    """
    List all roles
    """
    check_admin()

    roles = Role.query.all()
    return render_template('admin/roles/roles.html',
                            roles=roles, title='Roles')


@login_required
@admin.route('/roles/add', methods=['GET', 'POST'])
def add_role():
    """
    Add a role to the database
    """
    check_admin()

    add_role = True

    form = RoleForm()
    if form.validate_on_submit():
        role = Role(name=form.name.data,
                    description=form.description.data)
        
        try:
            # add role to the database
            db.session.add(role)
            db.session.commit()
            flash('You have successfully added a new role.')
        except:
            # in case role name already exists
            flash('Error: role name already exists.')

        # redirect to the roles page
        return redirect(url_for('admin.list_roles'))

    # load role template
    return render_template('admin/roles/role.html', add_role=add_role,
                            form=form, title='Add Role')


@login_required
@admin.route('roles/edit/<int:id>', methods=['GET', 'POST'])
def edit_role(id):
    """
    Edit a role
    """
    check_admin()

    add_role = False
    
    role = Role.query.get_or_404(id)
    form = RoleForm(obj=role)
    if form.validate_on_submit():
        role.name = form.name.data
        role.description = form.description.data
        db.session.add(role)
        db.session.commit()
        flash('You have successfully edited the role')

        # redirect to the roles page
        return redirect(url_for('admin.list_roles'))

    form.description.data = role.description
    form.name.data = role.name
    return render_template('admin/roles/role.html', add_role=add_role,
                            form=form, title="Edit Role")


@login_required
@admin.route('roles/delete/<int:id>', methods=['GET', 'POST'])
def delete_role(id):
    """
    Delete a role from the database
    """
    check_admin()

    role = Role.query.get_or_404(id)
    if role is not None:
        db.session.delete(role)
        db.session.commit()
        flash('You have successfully deleted the role.')

        # redirect to the roles page
        return redirect(url_for('admin.list_roles'))

    return render_template(title="Delete Role")


@login_required
@admin.route('/employess')
def list_employees():
    """
    List all employees
    """
    check_admin()

    employees = Employee.query.all()
    return render_template('admin/employees/employees.html',
                           employees=employees, title='Employees')


@login_required
@admin.route('/employees/assign/<int:id>', methods=['GET', 'POST'])
def assign_employee(id):
    """
    Assign a department and a role to an employee
    """
    check_admin()

    employee = Employee.query.get_or_404(id)

    # prevent admin from being assigned a department or role
    if employee.is_admin:
        abort(403)

    form = EmployeeAssignForm(obj=employee)
    if form.validate_on_submit():
        employee.department = form.department.data
        employee.role = form.role.data
        db.session.add(employee)
        db.session.commit()
        flash('You have successfully assigned a department and role.')

        # redirect to the roles page
        return redirect(url_for('admin.list_employees'))

    return render_template('admin/employees/employee.html',
                           employee=employee, form=form,
                           title='Assign Employee')