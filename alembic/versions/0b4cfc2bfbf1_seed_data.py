"""seed data

Revision ID: 0b4cfc2bfbf1
Revises: 221769d4e012
Create Date: 2026-03-25 19:25:09.018724

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0b4cfc2bfbf1'
down_revision: Union[str, Sequence[str], None] = '221769d4e012'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("INSERT INTO positions (name, compensation) VALUES" 
    "('Worker', 15.00),"
    "('Supervisor', 17.50),"
    "('Manager', 19.75)")

    op.execute("INSERT INTO employees (first_name, last_name, ssid, position_id, address, email, phone_number, emergency_contact, emergency_phone_number) VALUES"
               "('John', 'Doe', '123456789', 1, '123 Main St', 'john.doe@email.com', '780-123-4567', 'Jane Doe', '780-987-6543'),"
               "('Sarah', 'Smith', '987654321', 2, '456 Elm St', NULL, '780-234-5678', 'Bob Smith', '780-876-5432'),"
               "('Mike', 'Johnson', '456789123', 3, '789 Oak Ave', 'mike.j@email.com', '780-345-6789', 'Carol Johnson', '780-765-4321')")
    
    op.execute("INSERT INTO shifts (start_time, end_time, employee_id) VALUES"
               "('2024-01-15 08:00:00', '2024-01-15 16:00:00', 1),"
               "('2024-01-15 09:00:00', '2024-1-15 17:00:00', 2),"
               "('2024-01-15 07:00:00', '2024-01-15 15:00:00', 3)")

    op.execute("INSERT INTO time_records (clock_in_time, clock_out_time, employee_id) VALUES"
               "('2024-01-15 08:02:00', '2024-01-15 16:05:00', 1),"
               "('2024-01-15 09:01:00', '2024-01-15 17:03:00', 2),"
               "('2024-01-15 07:00:00', NULL, 3)")
    
    op.execute("INSERT INTO payroll (pay_period_start, pay_period_end, employee_id, total_hours_worked, total_pay) VALUES" \
                "('2024-01-01', '2024-01-15', 1, 40.00, 600.00)," 
                "('2024-01-01', '2024-01-15', 2, 40.00, 700),"
                "('2024-01-01', '2024-01-15', 3, 40.00, 790)")

def downgrade() -> None:
    op.execute("DELETE FROM payroll")
    op.execute("DELETE FROM time_records")
    op.execute("DELETE FROM shifts")
    op.execute("DELETE FROM employees")
    op.execute("DELETE FROM positions")
    
