from django.contrib.auth.hashers import make_password
from sqlalchemy.orm.exc import NoResultFound
from .models import session

from .models import Employee

class EmployeeAuthBackend(object):
    def authenticate(self, username=None, password=None):
        try:

            employee = session.query(Employee).filter_by(username=username).one()
            if employee.check_password(password):
                return employee

        except NoResultFound:
            return None


    def get_user(self, user_id):
        try:
            employee = session.query(Employee).filter_by(id=user_id).one()
        except NoResultFound:
            return None

        return employee
