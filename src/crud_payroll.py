from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from datetime import timedelta, datetime

from tables import Payroll, Employee, Shift

engine = create_engine('mysql+mysqldb://root:password@localhost:3306/module_6_assignment', echo=True)

def get_session():
        return Session(engine)
