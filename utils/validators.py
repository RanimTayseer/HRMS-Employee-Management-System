"""
validators.py - Data Validation Functions
"""

import re
from datetime import datetime


def is_valid_email(email):
    """Validate email address"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def is_valid_phone(phone):
    """Validate phone number"""
    pattern = r'^\+?[0-9]{10,15}$'
    return bool(re.match(pattern, phone))


def is_valid_salary(salary):
    """Validate salary amount"""
    try:
        salary = float(salary)
        return 0 <= salary <= 1000000
    except:
        return False


def is_valid_date(date_str):
    """Validate date format (YYYY-MM-DD)"""
    pattern = r'^\d{4}-\d{2}-\d{2}$'
    if not re.match(pattern, date_str):
        return False
    
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except:
        return False


def is_not_empty(value):
    """Check if field is not empty"""
    return value is not None and str(value).strip() != ""


def is_valid_employee_number(emp_number):
    """Validate employee number format"""
    pattern = r'^EMP\d{6}$'
    return bool(re.match(pattern, emp_number))