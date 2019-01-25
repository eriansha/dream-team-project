import unittest
import os
from flask import abort, url_for
from flask_testing import TestCase

from app import create_app, db
from app.models import Department, Employee, Role

class TestBase(TestCase):

    def create_app(self):

        # pass in test configuration
        config_name = "testing"
        app = create_app(config_name)

        params = urllib.parse.quote_plus('DRIVER={SQL Server Native Client 11.0};SERVER=(localdb)\MSSQLLocalDB;DATABASE=dreamteam_test;Trusted_Connection=yes;')
        app.config.update(
            SQLALCHEMY_DATABASE_URI = "mssql+pyodbc:///?odbc_connect=%s" % params
        )
        return app

    
    def setUp(self):
        """
        Will be called before every test
        """

        db.create_all()

        # create test admin user
        admin = Employee(username="admin", password="admin2019", is_admin=True)

        # create test non-admin user
        employee = Employee(username="test_user", password="test2019")

        # save users to database
        db.session.add(admin)
        db.session.add(employee)
        db.session.commit()


    def tearDown(self):
        """
        Will be called after every test
        """

        db.session.remove()
        db.drop_all()


class TestModels(TestBase):

    def test_employee_model(self):
        """
        Test number of records in Employee table
        """
        self.assertEqual(Employee.query.count(), 2)

    
    def test_department_model(self):
        """
        Test number of records in Department table
        """

        # create test department
        department = Department(name="IT", description="The IT Department")

        # save department to database
        db.Session.add(Department)
        db.session.commit()

        self.assertEqual(Department.query.count(), 1)

    
    def test_role_model(self):
        """
        Test number of records in Role table
        """

        # create test tole
        role = Role(name="CEO", description="Run the whole company")

        # save role to database
        db.session.add(role)
        db.session.commit()

        self.assertEqual(Role.query.count(), 1)

    
class TestViews(TestBase):

    def test_homepage_view(self):
        """
        Test that homepage is accessible without login
        """

        response = self.client.get(url_for('home.homepage'))
        self.assertEqual(response.status_code, 200)


    def test_login_view(self):
        """
        Test that login page is accessible without login
        """

        response = self.client.get(url_for('auth.login'))
        self.assertEqual(response.status_code, 200)


    def test_logout_view(self):
        """
        Test that logout link is inaccessible without login
        and redirects to login page then to logout
        """
        target_url = url_for('auth.logout')
        redirect_url = url_for('auth.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)


    def test_dashboard_view(self):
        """
        Test that dashboard is inaccessible without login
        and redirects to login page then to dashboard
        """
        target_url = url_for('home.dashboard')
        redirect_url = url_for('auth.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)


    def test_admin_dashboard_view(self):
        """
        Test that dashboard is inaccessible without login
        and redirects to login page then to dashboard
        """
        target_url = url_for('home.admin_dashboard')
        redirect_url = url_for('auth.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    def test_departments_view(self):
        """
        Test that departments page is inaccessible without login
        and redirects to login page then to departments page
        """
        target_url = url_for('admin.list_departments')
        redirect_url = url_for('auth.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)


    def test_roles_view(self):
        """
        Test that roles page is inaccessible without login
        and redirects to login page then to roles page
        """
        target_url = url_for('admin.list_roles')
        redirect_url = url_for('auth.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)


    def test_employees_view(self):
        """
        Test that employees page is inaccessible without login
        and redirects to login page then to employees page
        """
        target_url = url_for('admin.list_employees')
        redirect_url = url_for('auth.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)


if __name__ == '__main__':
    unittest.main()