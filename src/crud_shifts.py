from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from datetime import timedelta, datetime

from tables import Shift, Employee

engine = create_engine('mysql+mysqldb://root:password@localhost:3306/module_6_assignment', echo=True)

def get_session():
        return Session(engine)

def read_shifts():
    with get_session() as session:
        shifts = session.query(Shift).all()
        print("****Shift List****")
        for shift in shifts:
                print(f"""Shift ID: {shift.id} | Start Time: {shift.start_time} | End Time: {shift.end_time}
                    | Employee ID: {shift.employee_id}""")
        session.commit()
        session.close()

def get_shift_by_id(shift_id):
    with get_session() as session:
        shift = session.query(Shift).filter(Shift.id == shift_id).first()
        if not shift:
            print(f"Shift with ID {shift_id} not found!")
            return
        session.commit()
        print(f"""Shift ID {shift_id} | Start Time: {shift.start_time} | 
            End Time: {shift.end_time} | Employee ID: {shift.employee_id}""")
        session.close()

def get_shift_by_employee_id(employee_id):
    with get_session() as session:
        shifts = session.query(Shift).filter(Shift.employee_id == employee_id).all()
        if not shifts:
            print(f"Employee ID {employee_id} is not assigned a shift")
            return
        print(f"Employee ID {employee_id} Shifts:")
        for shift in shifts:
            print(f"""Shift ID: {shift.id} | Start Time: {shift.start_time} | End Time: {shift.end_time}""")
        session.commit()
        session.close()




def create_shift(start_time, employee_id):
    with get_session() as session:
            
        # dictionary created to loop through required conditions for validation
        conditions = {
            'start_time': start_time,
            'employee_id': employee_id
        }

        # validation on required fields that are left blank
        for key, value in conditions.items():# .items() used to to iterate over both keys and values
            if value == "":
                print(f"{key} cannot be empty!")
                return

        employee_id_check = session.query(Employee).filter(Employee.id == employee_id).first()
        if not employee_id_check:
            print(f"Employee ID {employee_id} not found")
            return

        new_shift = Shift(start_time=start_time, end_time = start_time + timedelta(hours=8), employee_id=employee_id)
        try:
            session.add(new_shift)
            session.commit()
            print(f"New shift has been added")
            session.close()
        except Exception as e:
            session.rollback()
            print(f"Error adding shift: {e}")

def update_shift(id, start_time=None, employee_id=None):
    with get_session() as session:
        shift = session.query(Shift).filter(Shift.id == id).first()

        if not start_time and not employee_id:
            print("No updates provided")
            return
        
        if not shift:
            print(f"Shift ID {id} does not exist")
            return
        
        if start_time:
            shift.start_time = start_time
            shift.end_time = shift.start_time + timedelta(hours=8)
        
        if employee_id:
            shift.employee_id = employee_id

        try:
            session.commit()
            session.close()
            print(f"Shift ID {id} has been updated")
        except Exception as e:
            session.rollback()
            print(f"Error updating shift: {e}")

def delete_shift(id):
    with get_session() as session:
        shift = session.query(Shift).filter(Shift.id == id).first()
        if not shift:
            print(f"Shift with ID {id} not found")
            return
        
        try:
            session.delete(shift)
            session.commit()
            print(f"Shift with ID {id} has been deleted")
            session.close()
        except Exception as e:
            session.rollback()
            print(f"Error deleting shift with id {e}")







# read_shifts()
# get_shift_by_employee_id(2)
# get_shift_by_id(1)

# create_shift(datetime(2026, 4, 5, 8, 0, 0), 2)
# read_shifts()
# get_shift_by_employee_id(2)
# get_shift_by_id(4)

# update_shift(4, datetime(2026, 5, 5, 8, 0, 0), 3)

# delete_shift(4)