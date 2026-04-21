"""
attendance.py - Attendance Model
"""

import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db_manager import db


class Attendance:
    """Attendance Management Class"""
    
    def __init__(self):
        self.db = db
    
    def check_in(self, employee_id):
        """Employee check-in"""
        today = datetime.now().strftime('%Y-%m-%d')
        now = datetime.now().strftime('%H:%M:%S')
        
        # Check if record exists for today
        existing = self.db.execute_query(
            "SELECT * FROM attendance WHERE employee_id = ? AND date = ?",
            (employee_id, today)
        )
        
        if existing:
            return False, "Already checked in today"
        
        result = self.db.execute_command(
            "INSERT INTO attendance (employee_id, date, check_in, status) VALUES (?, ?, ?, 'present')",
            (employee_id, today, now)
        )
        
        if result:
            return True, "Check-in successful"
        return False, "Check-in error occurred"
    
    def check_out(self, employee_id):
        """Employee check-out"""
        today = datetime.now().strftime('%Y-%m-%d')
        now = datetime.now().strftime('%H:%M:%S')
        
        # Find today's record
        record = self.db.execute_query(
            "SELECT * FROM attendance WHERE employee_id = ? AND date = ?",
            (employee_id, today)
        )
        
        if not record:
            return False, "No check-in found for today"
        
        if record[0].get('check_out'):
            return False, "Already checked out"
        
        result = self.db.execute_command(
            "UPDATE attendance SET check_out = ? WHERE attendance_id = ?",
            (now, record[0]['attendance_id'])
        )
        
        if result is not None:
            return True, "Check-out successful"
        return False, "Check-out error occurred"
    
    def get_today_attendance(self):
        """Get today's attendance"""
        today = datetime.now().strftime('%Y-%m-%d')
        return self.db.execute_query("""
            SELECT a.*, e.full_name, e.employee_number
            FROM attendance a
            JOIN employees e ON a.employee_id = e.employee_id
            WHERE a.date = ?
            ORDER BY e.full_name
        """, (today,))
    
    def get_by_employee(self, employee_id, month=None):
        """Get attendance for a specific employee"""
        query = "SELECT * FROM attendance WHERE employee_id = ?"
        params = [employee_id]
        
        if month:
            query += " AND strftime('%Y-%m', date) = ?"
            params.append(month)
        
        query += " ORDER BY date DESC"
        return self.db.execute_query(query, params)
    
    def get_monthly_summary(self, employee_id, year, month):
        """Get monthly attendance summary"""
        query = """
        SELECT 
            COUNT(*) as total_days,
            SUM(CASE WHEN status = 'present' THEN 1 ELSE 0 END) as present_days,
            SUM(CASE WHEN status = 'absent' THEN 1 ELSE 0 END) as absent_days,
            SUM(CASE WHEN status = 'late' THEN 1 ELSE 0 END) as late_days,
            SUM(CAST(total_hours AS REAL)) as total_hours,
            SUM(CAST(overtime_hours AS REAL)) as total_overtime,
            SUM(CAST(late_minutes AS INTEGER)) as total_late_minutes
        FROM attendance
        WHERE employee_id = ? 
        AND strftime('%Y', date) = ? 
        AND strftime('%m', date) = ?
        """
        result = self.db.execute_query(query, (employee_id, str(year), str(month).zfill(2)))
        return result[0] if result else None