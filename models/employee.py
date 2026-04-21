"""
employee.py - Employee Model
"""

import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db_manager import db


class Employee:
    """Employee Management Class"""
    
    def __init__(self):
        self.db = db
    
    def get_all(self):
        """Get all employees"""
        query = """
        SELECT e.*, d.department_name 
        FROM employees e
        LEFT JOIN departments d ON e.department_id = d.department_id
        WHERE e.status = 'active'
        ORDER BY e.full_name
        """
        return self.db.execute_query(query)
    
    def get_by_id(self, employee_id):
        """Get employee by ID"""
        query = "SELECT * FROM employees WHERE employee_id = ?"
        result = self.db.execute_query(query, (employee_id,))
        return result[0] if result else None
    
    def get_by_email(self, email):
        """Get employee by email"""
        query = "SELECT * FROM employees WHERE email = ?"
        result = self.db.execute_query(query, (email,))
        return result[0] if result else None
    
    def get_by_employee_number(self, emp_number):
        """Get employee by employee number"""
        query = "SELECT * FROM employees WHERE employee_number = ?"
        result = self.db.execute_query(query, (emp_number,))
        return result[0] if result else None
    
    def add(self, data):
        """Add new employee"""
        query = """
        INSERT INTO employees (
            employee_number, full_name, email, phone, address,
            department_id, position, basic_salary, hire_date, status
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'active')
        """
        result = self.db.execute_command(query, data)
        
        if result:
            try:
                from utils.session_manager import session
                from models.activity import ActivityModel
                activity = ActivityModel()
                activity.add_activity(
                    'add_employee',
                    f'New employee added: {data[1]}',
                    'employee'
                )
            except Exception as e:
                print(f"Activity log error: {e}")
        
        return result
    
    def update(self, employee_id, data):
        """Update employee data"""
        # Get old name for activity log
        old_employee = self.get_by_id(employee_id)
        old_name = old_employee.get('full_name', '') if old_employee else ''
        
        query = """
        UPDATE employees SET
            full_name = ?, email = ?, phone = ?, address = ?,
            department_id = ?, position = ?, basic_salary = ?
        WHERE employee_id = ?
        """
        params = list(data) + [employee_id]
        result = self.db.execute_command(query, params)
        
        if result:
            try:
                from models.activity import ActivityModel
                activity = ActivityModel()
                activity.add_activity(
                    'edit_employee',
                    f'Employee updated: {old_name} → {data[0]}',
                    'employee'
                )
            except Exception as e:
                print(f"Activity log error: {e}")
        
        return result
    
    def delete(self, employee_id):
        """Delete employee (change status only)"""
        # Get employee name for activity log
        employee = self.get_by_id(employee_id)
        emp_name = employee.get('full_name', '') if employee else ''
        
        query = "UPDATE employees SET status = 'deleted' WHERE employee_id = ?"
        result = self.db.execute_command(query, (employee_id,))
        
        if result:
            try:
                from models.activity import ActivityModel
                activity = ActivityModel()
                activity.add_activity(
                    'delete_employee',
                    f'Employee deleted: {emp_name}',
                    'employee'
                )
            except Exception as e:
                print(f"Activity log error: {e}")
        
        return result
    
    def search(self, keyword):
        """Search employees"""
        query = """
        SELECT e.*, d.department_name 
        FROM employees e
        LEFT JOIN departments d ON e.department_id = d.department_id
        WHERE e.full_name LIKE ? OR e.email LIKE ? OR e.employee_number LIKE ? OR e.phone LIKE ?
        """
        search_term = f"%{keyword}%"
        return self.db.execute_query(query, (search_term, search_term, search_term, search_term))
    
    def get_by_department(self, department_id):
        """Get employees by department"""
        query = """
        SELECT * FROM employees 
        WHERE department_id = ? AND status = 'active'
        """
        return self.db.execute_query(query, (department_id,))
    
    def get_active(self):
        """Get only active employees"""
        query = "SELECT * FROM employees WHERE status = 'active' ORDER BY full_name"
        return self.db.execute_query(query)
    
    def count_active(self):
        """Count active employees"""
        query = "SELECT COUNT(*) as count FROM employees WHERE status = 'active'"
        result = self.db.execute_query(query)
        return result[0]['count'] if result else 0
    
    def generate_employee_number(self):
        """Generate new employee number"""
        query = "SELECT MAX(CAST(SUBSTR(employee_number, 4) AS INTEGER)) as max_num FROM employees"
        result = self.db.execute_query(query)
        max_num = result[0]['max_num'] if result and result[0]['max_num'] else 0
        new_num = max_num + 1
        return f"EMP{str(new_num).zfill(6)}"