# Employee Time Tracking & Payroll System

## Overview

A command-line application for managing employee data, scheduling, and payroll for a small company. The system handles employee records, company positions, shift assignments, and clock in/out functionality with payroll processing.

## Features

- Add, read, update, and delete employee records, positions, and shifts
- Clock in/out validation that restricts check-in to a 15-minute window around shift start time
- Payroll processing based on configurable date windows

## Tech Stack

- Python
- SQLAlchemy ORM
- MariaDB
- Alembic (database migrations)
