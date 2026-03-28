from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from tables import Employee

engine = create_engine('mysql+mysqldb://root:password@localhost:3306/module_6_assignment', echo=True)

def get_session():
        return Session(engine)

def add_employee(first_name, last_name, ssid, position_id, address,
                  email, phone_number, emergency_contact, emergency_phone_number):
    with get_session() as session:

     # dictionary created to loop through required conditions for validation
        conditions = {
            'first_name': first_name,
            'last_name': last_name,
            'ssid': ssid,
            'position_id': position_id,
            'address': address,
            'phone_number': phone_number,
            'emergency_contact': emergency_contact,
            'emergency_phone_number': emergency_phone_number
            }
    
        # validation on required fields that are left blank
        for key, value in conditions.items(): # .items() used to to iterate over both keys and values
            if value == "":
                print(f"{key} cannot be blank!")
                return

        if not ssid.isdigit():
            print("SSID field must be numeric characters only!")
            return
        elif len(ssid) < 9 or len(ssid) > 9:
            print("SSID field must be 9 digits long!")
            return
        
        employee_new = Employee(first_name=first_name, last_name=last_name, ssid=ssid,
            position_id=position_id, address=address, email=email, phone_number=phone_number,
            emergency_contact=emergency_contact, emergency_phone_number=emergency_phone_number)
    
        try:
            session.add_all([employee_new])
            session.commit()
            print(f"New employee has been added")
            session.close()
        except Exception as e:
            session.rollback() # undoes partial changes that went through prior to error being flagged
            print(f"Error adding employee: {e}")

def read_employee():
    with get_session() as session:
        employees = session.query(Employee).all()
        print("****Employee List****")
        for employee in employees:
            print(f"""[ID: {employee.id}] Name: {employee.first_name} {employee.last_name} | SSID: {employee.ssid} | 
                Position ID: {employee.position_id} | Address: {employee.address} | Email: {employee.email} | Phone: {employee.phone_number} | 
                   Emergency Contact: {employee.emergency_contact} | Emergency Phone: {employee.emergency_phone_number}""")
        session.commit()
        session.close() 

def update_employee(id, first_name=None, last_name=None, ssid=None, position_id=None, address=None,
                  email=None, phone_number=None, emergency_contact=None, emergency_phone_number=None):
    with get_session() as session:
        employee = session.query(Employee).filter(Employee.id == id).first()

        if not employee:
            print(f"Employee with ID {id} does not exist")
            return

        if not any([first_name, last_name, ssid, position_id, address, 
            email, phone_number, emergency_contact, emergency_phone_number]):
            print("No updates provided")
            return

        if first_name:
            employee.first_name = first_name

        if last_name:
            employee.last_name = last_name

        if ssid:
            employee.ssid = ssid

        if position_id:
            employee.position_id = position_id

        if address:
            employee.address = address

        if email:
            employee.email = email

        if phone_number:
            employee.phone_number = phone_number

        if emergency_contact:
            employee.emergency_contact = emergency_contact

        if emergency_phone_number:
            employee.emergency_phone_number = emergency_phone_number

        try:
            session.commit()
            session.close()
            print(f"Employee with ID {id} has been updated!")
        except Exception as e:
            session.rollback()
            print(f"Error updating employee: {e}")  
            
def delete_employee(id):
    with get_session() as session:
        employee = session.query(Employee).filter(Employee.id == id).first()
        if not employee:
            print(f"Employee with id {id} not found")
            return
        try:
            session.delete(employee)
            session.commit()
            print(f"Employee with ID {employee.id} has been deleted")
            session.close()
        except Exception as e:
            session.rollback()
            print(f"Error deleting employee: {e}")


# Test data for functions

# add_employee('Ajay', 'Paterson', '002348529', 1, '123 ST NW', 'ajay@example.com',
#         '780-555-5555', 'Tiff', '780-998-8765')

# read_employee()
# delete_employee(4)