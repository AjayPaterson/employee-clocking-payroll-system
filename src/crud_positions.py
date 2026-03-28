from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from tables import Position

engine = create_engine('mysql+mysqldb://root:password@localhost:3306/module_6_assignment', echo=True)

def get_session():
        return Session(engine)

def add_position(name, compensation):
    with get_session() as session:
                
        if name == "":
            print(f"Name cannot be empty")
            return

        if compensation == "":
            print(f"Compensation cannot be empty")
            return
        try:
            compensation = float(compensation)
        except ValueError:
            print("Compensation must use a . (eg: 15.00)")
            return

        new_position = Position(name=name, compensation=compensation)

        try:
            session.add(new_position)
            session.commit()
            print(f"New position has been added")
            session.close()
        except Exception as e:
            session.rollback()
            print(f"Error adding position: {e}")


def update_position(id, name=None, compensation=None):
    with get_session() as session:
        position = session.query(Position).filter(Position.id == id).first()

        if not position:
            print(f"Position with ID {id} does not exist")
            return

        if not name and not compensation:
            print("No updates provided")
            return

        if name:
            position.name = name

        if compensation:
            position.compensation = compensation

        try:
            session.commit()
            session.close()
            print(f"Position ID {id} has been updated")
        except Exception as e:
            session.rollback()
            print(f"Error updating position: {e}")            


def read_positions():
    with get_session() as session:
        positions = session.query(Position).all()
        print(f"****Position List****")
        for position in positions:
            print(f"Position ID: {position.id} | Position Name: {position.name} | Compensation: {position.compensation}")
        session.commit()
        session.close()


def delete_position(id):
    with get_session() as session:
        position = session.query(Position).filter(Position.id == id).first()
        if not position:
            print(f"Position with ID {id} not found")
            return

        try:
            session.delete(position)
            session.commit()
            print(f"Position with ID {id} has been deleted")
            session.close()
        except Exception as e:
            session.rollback()
            print(f"Error deleting position: {e}")
        


# Test data for functions

# read_positions()

# add_position("Assistant Manager", 18.00)

# update_position(4, None, 18.25)

# delete_position(4)