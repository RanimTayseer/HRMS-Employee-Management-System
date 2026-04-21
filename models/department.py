"""
department.py - Department Model
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db_manager import db


class Department:
    """Department Management Class"""
    
    def __init__(self):
        self.db = db
    
    def get_all(self):
        """Get all departments"""
        query = """
        SELECT d.*, 
               COUNT(e.employee_id) as employee_count
        FROM departments d
        LEFT JOIN employees e ON d.department_id = e.department_id AND e.status = 'active'
        WHERE d.is_active = 1
        GROUP BY d.department_id
        ORDER BY d.department_name
        """
        return self.db.execute_query(query)
    
    def get_by_id(self, department_id):
        """Get department by ID"""
        query = "SELECT * FROM departments WHERE department_id = ?"
        result = self.db.execute_query(query, (department_id,))
        return result[0] if result else None
    
    def add(self, data):
        """Add new department"""
        query = """
        INSERT INTO departments (department_code, department_name, description, is_active)
        VALUES (?, ?, ?, 1)
        """
        return self.db.execute_command(query, data)
    
    def update(self, department_id, data):
        """Update department data"""
        query = """
        UPDATE departments SET
            department_code = ?,
            department_name = ?,
            description = ?
        WHERE department_id = ?
        """
        params = list(data) + [department_id]
        return self.db.execute_command(query, params)
    
    def delete(self, department_id):
        """Delete department"""
        query = "DELETE FROM departments WHERE department_id = ?"
        return self.db.execute_command(query, (department_id,))
    
    def count(self):
        """Get number of departments"""
        query = "SELECT COUNT(*) as count FROM departments WHERE is_active = 1"
        result = self.db.execute_query(query)
        return result[0]['count'] if result else 0