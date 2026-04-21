"""
report.py - Report Model (with Arabic language support)
"""

import sys
import os
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from bidi.algorithm import get_display
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db_manager import db
from models.employee import Employee
from models.attendance import Attendance
from models.leave import LeaveModel
from models.payroll import Payroll

# ============================================================
# Register Arabic font
# ============================================================

ARABIC_FONT_AVAILABLE = False
ARABIC_FONT_NAME = 'Helvetica'

try:
    font_path = "C:/Windows/Fonts/arial.ttf"
    if os.path.exists(font_path):
        pdfmetrics.registerFont(TTFont('ArabicFont', font_path))
        ARABIC_FONT_AVAILABLE = True
        ARABIC_FONT_NAME = 'ArabicFont'
        print("✅ Arabic font (Arial) loaded successfully")
except Exception as e:
    print(f"⚠️ Failed to load font: {e}")


class Report:
    """Report Management Class"""
    
    def __init__(self):
        self.db = db
        self.employee_model = Employee()
        self.attendance_model = Attendance()
        self.leave_model = LeaveModel()
        self.payroll_model = Payroll()
    
    def arabic_text(self, text):
        """Convert Arabic text for proper display in PDF"""
        if not text:
            return ""
        return get_display(text)
    
    def get_style(self, styles, size=12, bold=False, alignment=TA_RIGHT):
        """Create style that supports Arabic language"""
        font_name = ARABIC_FONT_NAME if ARABIC_FONT_AVAILABLE else 'Helvetica'
        
        return ParagraphStyle(
            'CustomStyle',
            parent=styles['Normal'],
            fontName=font_name,
            fontSize=size,
            alignment=alignment,
            encoding='utf-8'
        )
    
    def generate_employees_report(self, filename):
        """Generate employees report PDF"""
        employees = self.employee_model.get_all()
        
        doc = SimpleDocTemplate(filename, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
        elements = []
        
        styles = getSampleStyleSheet()
        
        # Report title
        title_style = self.get_style(styles, size=20, bold=True, alignment=TA_CENTER)
        title = Paragraph(self.arabic_text("Employees Report"), title_style)
        elements.append(title)
        elements.append(Spacer(1, 20))
        
        # Date
        date_style = self.get_style(styles, size=10, alignment=TA_CENTER)
        date_text = Paragraph(self.arabic_text(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}"), date_style)
        elements.append(date_text)
        elements.append(Spacer(1, 20))
        
        # Statistics
        stats_data = [
            [self.arabic_text("Total Employees"), str(len(employees))],
            [self.arabic_text("Active Employees"), str(self.employee_model.count_active())],
        ]
        
        stats_table = Table(stats_data, colWidths=[150, 100])
        stats_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 0), (-1, -1), ARABIC_FONT_NAME if ARABIC_FONT_AVAILABLE else 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ]))
        elements.append(stats_table)
        elements.append(Spacer(1, 20))
        
        # Employees table
        table_data = [
            ['#', self.arabic_text("Employee ID"), self.arabic_text("Name"), 
             self.arabic_text("Department"), self.arabic_text("Position"), self.arabic_text("Salary")]
        ]
        
        for i, emp in enumerate(employees, 1):
            table_data.append([
                str(i),
                emp.get('employee_number', ''),
                self.arabic_text(emp.get('full_name', '')),
                self.arabic_text(emp.get('department_name', '')),
                self.arabic_text(emp.get('position', '')),
                f"{emp.get('basic_salary', 0):,.2f}"
            ])
        
        table = Table(table_data, colWidths=[40, 90, 120, 100, 100, 100])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), ARABIC_FONT_NAME if ARABIC_FONT_AVAILABLE else 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('FONTNAME', (0, 1), (-1, -1), ARABIC_FONT_NAME if ARABIC_FONT_AVAILABLE else 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(table)
        
        doc.build(elements)
        return True
    
    def generate_attendance_report(self, filename, month=None):
        """Generate attendance report PDF"""
        if not month:
            month = datetime.now().strftime('%Y-%m')
        
        query = """
        SELECT a.*, e.full_name, e.employee_number, d.department_name
        FROM attendance a
        JOIN employees e ON a.employee_id = e.employee_id
        LEFT JOIN departments d ON e.department_id = d.department_id
        WHERE strftime('%Y-%m', a.date) = ?
        ORDER BY e.full_name, a.date
        """
        attendance = self.db.execute_query(query, (month,))
        
        doc = SimpleDocTemplate(filename, pagesize=landscape(A4))
        elements = []
        
        styles = getSampleStyleSheet()
        
        title_style = self.get_style(styles, size=18, bold=True, alignment=TA_CENTER)
        title = Paragraph(self.arabic_text(f"Attendance Report - {month}"), title_style)
        elements.append(title)
        elements.append(Spacer(1, 20))
        
        date_style = self.get_style(styles, size=10, alignment=TA_CENTER)
        date_text = Paragraph(self.arabic_text(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}"), date_style)
        elements.append(date_text)
        elements.append(Spacer(1, 20))
        
        # Attendance table
        table_data = [
            ['#', self.arabic_text("Employee"), self.arabic_text("Department"), 
             self.arabic_text("Date"), self.arabic_text("Check In"), 
             self.arabic_text("Check Out"), self.arabic_text("Status")]
        ]
        
        for i, att in enumerate(attendance, 1):
            table_data.append([
                str(i),
                self.arabic_text(att.get('full_name', '')),
                self.arabic_text(att.get('department_name', '')),
                att.get('date', ''),
                att.get('check_in', ''),
                att.get('check_out', ''),
                self.arabic_text(att.get('status', ''))
            ])
        
        table = Table(table_data, colWidths=[40, 120, 100, 80, 60, 60, 80])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), ARABIC_FONT_NAME if ARABIC_FONT_AVAILABLE else 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('FONTNAME', (0, 1), (-1, -1), ARABIC_FONT_NAME if ARABIC_FONT_AVAILABLE else 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(table)
        
        doc.build(elements)
        return True
    
    def generate_salary_report(self, filename, month=None):
        """Generate salary report PDF"""
        if not month:
            month = datetime.now().strftime('%Y-%m')
        
        payrolls = self.payroll_model.get_by_month(month)
        
        doc = SimpleDocTemplate(filename, pagesize=A4)
        elements = []
        
        styles = getSampleStyleSheet()
        
        title_style = self.get_style(styles, size=18, bold=True, alignment=TA_CENTER)
        title = Paragraph(self.arabic_text(f"Salary Report - {month}"), title_style)
        elements.append(title)
        elements.append(Spacer(1, 20))
        
        date_style = self.get_style(styles, size=10, alignment=TA_CENTER)
        date_text = Paragraph(self.arabic_text(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}"), date_style)
        elements.append(date_text)
        elements.append(Spacer(1, 20))
        
        # Statistics
        total_salaries = sum([p.get('net_salary', 0) or 0 for p in payrolls])
        total_deductions = sum([p.get('deductions', 0) or 0 for p in payrolls])
        
        stats_data = [
            [self.arabic_text("Number of Employees"), str(len(payrolls))],
            [self.arabic_text("Total Salaries"), f"{total_salaries:,.2f}"],
            [self.arabic_text("Total Deductions"), f"{total_deductions:,.2f}"],
        ]
        
        stats_table = Table(stats_data, colWidths=[150, 150])
        stats_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 0), (-1, -1), ARABIC_FONT_NAME if ARABIC_FONT_AVAILABLE else 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ]))
        elements.append(stats_table)
        elements.append(Spacer(1, 20))
        
        # Salary table
        table_data = [
            ['#', self.arabic_text("Employee"), self.arabic_text("Department"), 
             self.arabic_text("Basic Salary"), self.arabic_text("Allowances"), 
             self.arabic_text("Deductions"), self.arabic_text("Net Salary")]
        ]
        
        for i, p in enumerate(payrolls, 1):
            table_data.append([
                str(i),
                self.arabic_text(p.get('full_name', '')),
                self.arabic_text(p.get('department_name', '')),
                f"{p.get('basic_salary', 0):,.2f}",
                f"{p.get('allowances', 0):,.2f}",
                f"{p.get('deductions', 0):,.2f}",
                f"{p.get('net_salary', 0):,.2f}"
            ])
        
        table = Table(table_data, colWidths=[40, 120, 100, 100, 100, 100, 120])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), ARABIC_FONT_NAME if ARABIC_FONT_AVAILABLE else 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('FONTNAME', (0, 1), (-1, -1), ARABIC_FONT_NAME if ARABIC_FONT_AVAILABLE else 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(table)
        
        doc.build(elements)
        return True
    
    def generate_charts(self, filename):
        """Generate statistical charts"""
        query = """
        SELECT d.department_name, COUNT(e.employee_id) as count
        FROM departments d
        LEFT JOIN employees e ON d.department_id = e.department_id AND e.status = 'active'
        GROUP BY d.department_id
        """
        dept_data = self.db.execute_query(query)
        
        departments = [d['department_name'] for d in dept_data]
        counts = [d['count'] for d in dept_data]
        
        # Configure Arabic font for charts
        plt.rcParams['font.sans-serif'] = ['Arial', 'Tahoma']
        plt.rcParams['axes.unicode_minus'] = False
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        colors_list = ['#3498db', '#2ecc71', '#e74c3c', '#f39c12', '#9b59b6']
        bars = ax1.bar(departments, counts, color=colors_list[:len(departments)])
        ax1.set_xlabel('Departments', fontsize=12)
        ax1.set_ylabel('Number of Employees', fontsize=12)
        ax1.set_title('Employee Distribution by Department', fontsize=14)
        ax1.tick_params(axis='x', rotation=45)
        
        for bar, count in zip(bars, counts):
            ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                    str(count), ha='center', va='bottom')
        
        ax2.pie(counts, labels=departments, autopct='%1.1f%%', colors=colors_list[:len(departments)])
        ax2.set_title('Employee Percentage by Department', fontsize=14)
        
        plt.tight_layout()
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        
        return True