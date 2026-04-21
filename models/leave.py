"""
leave.py - Leave Model
"""

import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db_manager import db


class LeaveModel:
    """Leave Management Class"""
    
    def __init__(self):
        self.db = db
    
    def request(self, employee_id, leave_type, start_date, end_date, reason):
        """Submit leave request"""
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
        days = (end - start).days + 1
        
        result = self.db.execute_command("""
            INSERT INTO leaves (employee_id, leave_type, start_date, end_date, days_count, reason, status)
            VALUES (?, ?, ?, ?, ?, ?, 'pending')
        """, (employee_id, leave_type, start_date, end_date, days, reason))
        
        if result:
            return True, "Leave request submitted successfully"
        return False, "Error submitting leave request"
    
    def get_pending(self):
        """Get pending leave requests"""
        return self.db.execute_query("""
            SELECT l.*, e.full_name, e.employee_number, d.department_name
            FROM leaves l
            JOIN employees e ON l.employee_id = e.employee_id
            LEFT JOIN departments d ON e.department_id = d.department_id
            WHERE l.status = 'pending'
            ORDER BY l.created_at ASC
        """)
    
    def get_all(self):
        """Get all leave requests"""
        return self.db.execute_query("""
            SELECT l.*, e.full_name, e.employee_number
            FROM leaves l
            JOIN employees e ON l.employee_id = e.employee_id
            ORDER BY l.created_at DESC
        """)
    
    def get_by_employee(self, employee_id):
        """Get leave requests by employee"""
        return self.db.execute_query("""
            SELECT * FROM leaves
            WHERE employee_id = ?
            ORDER BY created_at DESC
        """, (employee_id,))
    
    def update_status(self, leave_id, status):
        """Update leave status (approve or reject)"""
        result = self.db.execute_command("""
            UPDATE leaves SET status = ?, approved_at = CURRENT_TIMESTAMP
            WHERE leave_id = ?
        """, (status, leave_id))
        
        if result is not None:
            return True, f"Leave {status} successfully"
        return False, "An error occurred"
    
    def approve(self, leave_id):
        """Approve leave request"""
        return self.update_status(leave_id, 'approved')
    
    def reject(self, leave_id):
        """Reject leave request"""
        return self.update_status(leave_id, 'rejected')
    
    def get_balance(self, employee_id):
        """Calculate remaining leave balance"""
        current_year = datetime.now().strftime('%Y')
        query = """
        SELECT COALESCE(SUM(days_count), 0) as used_days
        FROM leaves
        WHERE employee_id = ? 
        AND status = 'approved'
        AND strftime('%Y', start_date) = ?
        AND leave_type = 'annual'
        """
        result = self.db.execute_query(query, (employee_id, current_year))
        used_days = result[0]['used_days'] if result else 0
        
        total_days = 21
        remaining = total_days - used_days
        
        return {
            'total_days': total_days,
            'used_days': used_days,
            'remaining_days': remaining if remaining > 0 else 0
        }