from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from datetime import timedelta, datetime

from tables import TimeRecord, Employee, Shift

engine = create_engine('mysql+mysqldb://root:password@localhost:3306/module_6_assignment', echo=True)

def get_session():
        return Session(engine)

# creates new record
def create_check_in(employee_id, check_in_time = None):
    with get_session() as session:

        if check_in_time is None:
             check_in_time = datetime.now()

        employee = session.query(Employee).filter(Employee.id == employee_id).first()
        
        if not employee:
            print(f"Employee ID: {employee_id} does not exist")
            return

        shift_start = session.query(Shift).filter(Shift.employee_id == employee_id,
                                                Shift.start_time >= check_in_time - timedelta(minutes=15),
                                                Shift.start_time <= check_in_time + timedelta(minutes=15)).first()        

        if not shift_start:
            print(f"Employee {employee_id} cannot clock in at {check_in_time} No shift found withithin allowed 15 minute window.")
            return

        time_record = TimeRecord(clock_in_time=check_in_time, employee_id=employee_id)

        try:
            session.add(time_record)
            session.commit()
            print(f"{employee_id} has checked in!")
        except Exception as e:
            session.rollback()
            print(f"Error checking in: {e}")

# updates existing record with check_out_time data
def create_check_out(employee_id, check_out_time=None):
    with get_session() as session:
          
        if check_out_time is None:
            check_out_time = datetime.now()
        
        employee = session.query(Employee).filter(Employee.id == employee_id).first()
        
        if not employee:
            print(f"Employee ID: {employee_id} does not exist")
            return

        check_out = session.query(TimeRecord).filter(TimeRecord.employee_id == employee_id, 
                                    TimeRecord.clock_out_time == None).first()

        if check_out is None:
            print(f"Employee hasn't clocked in yet")
            return

        check_out.clock_out_time = check_out_time

        try:
            session.commit()
            print(f"Employe ID: {employee_id} has clocked out!")
            session.close()
        except Exception as e:
            session.rollback()
            print(f"Error ending shift: {e}")


def read_time_records():
    with get_session() as session:
        time_record = session.query(TimeRecord).all()
        print("***Time Records List****")
        for record in time_record:
            print(f"""Record ID: {record.id} | Employee ID: {record.employee_id} | Clocked In: {record.clock_in_time} | 
                Clocked out: {record.clock_out_time}""")
        session.close()


def delete_time_record(id):
    with get_session() as session:
        record = session.query(TimeRecord).filter(TimeRecord.id == id).first()
        if not record:
            print(f"Time Record with ID {id} not found")
            return
        
        try:
            session.delete(record)
            session.commit()
            print(f"Record with ID {id} has been deleted")
            session.close()
        except Exception as e:
            session.rollback()
            print(f"Error deleting record: {e}")

            
# create_check_in(3, datetime(2024,1, 15, 7, 5,0))

# create_check_out(3)