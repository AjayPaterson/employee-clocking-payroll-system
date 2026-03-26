from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DATETIME, DECIMAL, DATE
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
from datetime import datetime

engine = create_engine('mysql+mysqldb://root:password@localhost:3306/module_6_assignment', echo=True)

Base = declarative_base()

class Employee(Base):
    __tablename__ = 'employees'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    ssid = Column(String(9), nullable=False)
    position_id = Column(Integer, ForeignKey('positions.id'), nullable=False)
    address = Column(String(100), nullable=False)
    email = Column(String(100))
    phone_number = Column(String(25), nullable=False)
    emergency_contact = Column(String(100), nullable=False)
    emergency_phone_number = Column(String(25), nullable=False)

    position = relationship('Position', back_populates='employees')
    shifts = relationship('Shift', back_populates='employee')
    time_records = relationship('TimeRecord', back_populates='employee')
    payroll = relationship('Payroll', back_populates='employee')

class Position(Base):
    __tablename__ = 'positions'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    compensation = Column(DECIMAL(5,2), nullable=False)

    employees = relationship('Employee', back_populates='position')

class Shift(Base):
    __tablename__ = 'shifts'
    id = Column(Integer, primary_key=True)
    start_time = Column(DATETIME, nullable=False)
    end_time = Column(DATETIME, nullable=False)
    employee_id = Column(Integer, ForeignKey('employees.id'), nullable=False)

    employee = relationship("Employee", back_populates='shifts')

class TimeRecord(Base):
    __tablename__ = 'time_records'
    id = Column(Integer, primary_key=True)
    clock_in_time = Column(DATETIME, nullable=False)
    clock_out_time = Column(DATETIME)
    employee_id = Column(Integer, ForeignKey('employees.id'), nullable=False)

    employee = relationship('Employee', back_populates='time_records')

class Payroll(Base):
    __tablename__ = 'payroll'
    id = Column(Integer, primary_key=True)
    pay_period_start = Column(DATE, nullable=False)
    pay_period_end = Column(DATE, nullable=False)
    employee_id = Column(Integer, ForeignKey('employees.id'), nullable=False)
    total_hours_worked = Column(DECIMAL(5,2), nullable=False)
    total_pay = Column(DECIMAL(7,2), nullable=False)

    employee = relationship('Employee', back_populates='payroll')

