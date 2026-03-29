from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from datetime import datetime
from decimal import Decimal


from tables import Payroll, Employee, TimeRecord

engine = create_engine('mysql+mysqldb://root:password@localhost:3306/module_6_assignment', echo=True)

def get_session():
        return Session(engine)

def create_payroll(start_date, end_date, employee_id):
    with get_session() as session:
        
        # Check to see if Employee ID exists
        check_employee_id = session.query(Employee).filter(Employee.id == employee_id).first()
        if not check_employee_id:
            print(f"Employee ID: {employee_id} not found.")
            return

        payroll_record = session.query(TimeRecord).filter(TimeRecord.clock_in_time >= start_date, 
                                                    TimeRecord.clock_in_time <= end_date,
                                                    TimeRecord.employee_id == employee_id).all()
        
        # checks all records have been dates filled in
        if not payroll_record:
            print(f"No payroll records found within {start_date} and {end_date}")
            return
                
        total_hours = 0
        for record in payroll_record:
            if record.clock_out_time is None:
                print(f"Employee hasn't clocked out of all shifts!")
                return

            hours_worked_per_shift = (record.clock_out_time - record.clock_in_time).total_seconds() / 3600
            total_hours += hours_worked_per_shift
                
        employee_pay = check_employee_id.position.compensation * Decimal(str(total_hours)) # use str() to convert to string first to avoid floating point issues.

        new_payroll_record = Payroll(pay_period_start=start_date, pay_period_end=end_date, 
                                    employee_id=employee_id, total_hours_worked=total_hours, 
                                    total_pay=employee_pay)
        
        try:
            session.add(new_payroll_record)
            session.commit()
            print(f"Payroll record added!")
            session.close()
        except Exception as e:
             session.rollback()
             print(f"Error adding payroll record: {e}")


def read_payroll_record_by_employee(employee_id):
    with get_session() as session:
        records = session.query(Payroll).filter(Payroll.employee_id == employee_id).all()
        if not records:
            print(f"Employee ID {employee_id} has no payroll record")
            return
        for record in records:
        
            print(f"""Employee ID {employee_id} | Shift ID: {record.id}  | 
                Pay Period Start-End {record.pay_period_start}-{record.pay_period_end} | 
                Hours Worked: {record.total_hours_worked}| Pay: {record.total_pay}""")
        session.commit()
        session.close()



# Test date for functions

# create_payroll(datetime(2026,5,1), datetime(2026,5,15), 3)

# read_payroll_record_by_employee(3)