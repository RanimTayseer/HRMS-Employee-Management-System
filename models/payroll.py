"""
payroll.py - Payroll Model
"""

import sys
import os
from datetime import datetime
from calendar import monthrange

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db_manager import db
from models.attendance import Attendance
from models.employee import Employee


class Payroll:
    """Payroll Management Class"""
    
    def __init__(self):
        self.db = db
        self.attendance_model = Attendance()
        self.employee_model = Employee()
    
    def get_all(self, month=None):
        """Get all payroll records"""
        query = """
        SELECT p.*, e.full_name, e.employee_number, d.department_name
        FROM payroll p
        JOIN employees e ON p.employee_id = e.employee_id
        LEFT JOIN departments d ON e.department_id = d.department_id
        WHERE 1=1
        """
        params = []
        
        if month:
            query += " AND p.month = ?"
            params.append(month)
        
        query += " ORDER BY p.created_at DESC"
        
        return self.db.execute_query(query, params if params else None)
    
    def get_by_employee(self, employee_id, month=None):
        """Get payroll records for a specific employee"""
        query = "SELECT * FROM payroll WHERE employee_id = ?"
        params = [employee_id]
        
        if month:
            query += " AND month = ?"
            params.append(month)
        
        query += " ORDER BY month DESC"
        
        return self.db.execute_query(query, params)
    
    def get_by_month(self, month):
        """Get payroll records for a specific month"""
        query = """
        SELECT p.*, e.full_name, e.employee_number, d.department_name
        FROM payroll p
        JOIN employees e ON p.employee_id = e.employee_id
        LEFT JOIN departments d ON e.department_id = d.department_id
        WHERE p.month = ?
        ORDER BY e.full_name
        """
        return self.db.execute_query(query, (month,))
    
    def calculate_salary(self, employee_id, month):
        """Calculate salary for an employee for a specific month"""
        # Get employee data
        employee = self.employee_model.get_by_id(employee_id)
        
        if not employee:
            return None
        
        basic_salary = employee.get('basic_salary', 0) or 0
        housing_allowance = employee.get('housing_allowance', 0) or 0
        transport_allowance = employee.get('transport_allowance', 0) or 0
        
        # Calculate days in month
        year, month_num = map(int, month.split('-'))
        days_in_month = monthrange(year, month_num)[1]
        
        # Get attendance summary
        summary = self.attendance_model.get_monthly_summary(employee_id, year, month_num)
        
        absent_days = summary['absent_days'] if summary else 0
        late_minutes = summary['total_late_minutes'] if summary else 0
        overtime_hours = summary['total_overtime'] if summary else 0
        
        # Calculations
        daily_rate = basic_salary / days_in_month if days_in_month > 0 else 0
        
        deduction_absent = daily_rate * absent_days
        deduction_late = (basic_salary / (days_in_month * 8 * 60)) * late_minutes if days_in_month > 0 else 0
        overtime_amount = (basic_salary / (days_in_month * 8)) * overtime_hours * 1.5 if days_in_month > 0 else 0
        
        allowances = housing_allowance + transport_allowance
        deductions = deduction_absent + deduction_late
        bonus = 0
        
        net_salary = basic_salary + allowances + overtime_amount + bonus - deductions
        
        return {
            'employee_id': employee_id,
            'month': month,
            'basic_salary': basic_salary,
            'allowances': allowances,
            'overtime_amount': overtime_amount,
            'bonus': bonus,
            'deductions': deductions,
            'net_salary': net_salary,
            'absent_days': absent_days,
            'late_minutes': late_minutes,
            'overtime_hours': overtime_hours
        }
    
    def process_payroll(self, month, employee_id=None):
        """Process payroll for a specific month"""
        if employee_id:
            salary = self.calculate_salary(employee_id, month)
            if not salary:
                return None
            
            # Check if payroll exists for this month
            check_query = "SELECT * FROM payroll WHERE employee_id = ? AND month = ?"
            existing = self.db.execute_query(check_query, (employee_id, month))
            
            if existing:
                # Update
                query = """
                UPDATE payroll SET
                    basic_salary = ?, allowances = ?, overtime_amount = ?,
                    bonus = ?, deductions = ?, net_salary = ?
                WHERE employee_id = ? AND month = ?
                """
                params = (
                    salary['basic_salary'],
                    salary['allowances'],
                    salary['overtime_amount'],
                    salary['bonus'],
                    salary['deductions'],
                    salary['net_salary'],
                    employee_id,
                    month
                )
            else:
                # Insert new
                query = """
                INSERT INTO payroll (
                    employee_id, month, basic_salary, allowances,
                    overtime_amount, bonus, deductions, net_salary
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """
                params = (
                    employee_id,
                    month,
                    salary['basic_salary'],
                    salary['allowances'],
                    salary['overtime_amount'],
                    salary['bonus'],
                    salary['deductions'],
                    salary['net_salary']
                )
            
            return self.db.execute_command(query, params)
        else:
            # Process all employees
            employees = self.employee_model.get_active()
            processed = 0
            
            for emp in employees:
                result = self.process_payroll(month, emp['employee_id'])
                if result:
                    processed += 1
            
            return processed
    
    def mark_as_paid(self, payroll_id):
        """Mark salary as paid"""
        query = "UPDATE payroll SET paid_at = CURRENT_TIMESTAMP WHERE payroll_id = ?"
        return self.db.execute_command(query, (payroll_id,))
    
    def get_monthly_summary(self, month):
        """Get monthly payroll summary"""
        query = """
        SELECT 
            COUNT(*) as total_employees,
            SUM(net_salary) as total_salaries,
            SUM(allowances) as total_allowances,
            SUM(deductions) as total_deductions,
            SUM(overtime_amount) as total_overtime,
            AVG(net_salary) as average_salary
        FROM payroll
        WHERE month = ?
        """
        result = self.db.execute_query(query, (month,))
        return result[0] if result else None
    
    def get_available_months(self):
        """Get list of available months in payroll"""
        query = "SELECT DISTINCT month FROM payroll ORDER BY month DESC"
        return self.db.execute_query(query)