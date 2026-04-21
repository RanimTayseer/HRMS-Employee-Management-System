"""
email_notifier.py - Email Notification System
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import threading


class EmailNotifier:
    """Email notification manager"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.smtp_server = "smtp.gmail.com"
            cls._instance.smtp_port = 587
            cls._instance.sender_email = ""
            cls._instance.sender_password = ""
            cls._instance.enabled = False
        return cls._instance
    
    def configure(self, email, password, enabled=True):
        """Configure email settings"""
        self.sender_email = email
        self.sender_password = password
        self.enabled = enabled
    
    def send_email(self, to_email, subject, body):
        """Send email asynchronously"""
        if not self.enabled or not self.sender_email:
            print("Email notifications disabled or not configured")
            return False
        
        def send():
            try:
                msg = MIMEMultipart()
                msg['From'] = self.sender_email
                msg['To'] = to_email
                msg['Subject'] = subject
                
                msg.attach(MIMEText(body, 'html', 'utf-8'))
                
                server = smtplib.SMTP(self.smtp_server, self.smtp_port)
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
                server.quit()
                print(f"Email sent to {to_email}")
            except Exception as e:
                print(f"Failed to send email: {e}")
        
        # Send in background thread
        thread = threading.Thread(target=send)
        thread.daemon = True
        thread.start()
        return True
    
    def send_new_employee_notification(self, admin_email, employee_data):
        """Send notification when new employee is added"""
        subject = f"New Employee Added: {employee_data.get('full_name', '')}"
        body = f"""
        <html>
        <body style="font-family: Arial, sans-serif;">
            <h2 style="color: #2c3e50;">New Employee Added</h2>
            <p>A new employee has been added to the system.</p>
            <table style="border-collapse: collapse; width: 100%;">
                <tr style="background-color: #3498db; color: white;">
                    <th style="padding: 10px; text-align: left;">Field</th>
                    <th style="padding: 10px; text-align: left;">Value</th>
                </tr>
                <tr style="background-color: #ecf0f1;">
                    <td style="padding: 8px;"><strong>Name</strong></td>
                    <td style="padding: 8px;">{employee_data.get('full_name', '')}</td>
                </tr>
                <tr>
                    <td style="padding: 8px;"><strong>Email</strong></td>
                    <td style="padding: 8px;">{employee_data.get('email', '')}</td>
                </tr>
                <tr style="background-color: #ecf0f1;">
                    <td style="padding: 8px;"><strong>Position</strong></td>
                    <td style="padding: 8px;">{employee_data.get('position', '')}</td>
                </tr>
                <tr>
                    <td style="padding: 8px;"><strong>Department</strong></td>
                    <td style="padding: 8px;">{employee_data.get('department_name', '')}</td>
                </tr>
                <tr style="background-color: #ecf0f1;">
                    <td style="padding: 8px;"><strong>Basic Salary</strong></td>
                    <td style="padding: 8px;">{employee_data.get('basic_salary', 0):,.2f}</td>
                </tr>
                <tr>
                    <td style="padding: 8px;"><strong>Hire Date</strong></td>
                    <td style="padding: 8px;">{employee_data.get('hire_date', '')}</td>
                </tr>
            </table>
            <p style="margin-top: 20px; color: #7f8c8d;">This is an automated message from the HRMS system.</p>
        </body>
        </html>
        """
        return self.send_email(admin_email, subject, body)
    
    def send_leave_request_notification(self, manager_email, leave_data):
        """Send notification when leave is requested"""
        subject = f"Leave Request: {leave_data.get('employee_name', '')}"
        body = f"""
        <html>
        <body style="font-family: Arial, sans-serif;">
            <h2 style="color: #2c3e50;">Leave Request Pending Approval</h2>
            <p>An employee has submitted a leave request.</p>
            <table style="border-collapse: collapse; width: 100%;">
                <tr style="background-color: #3498db; color: white;">
                    <th style="padding: 10px; text-align: left;">Field</th>
                    <th style="padding: 10px; text-align: left;">Value</th>
                </tr>
                <tr style="background-color: #ecf0f1;">
                    <td style="padding: 8px;"><strong>Employee</strong></td>
                    <td style="padding: 8px;">{leave_data.get('employee_name', '')}</td>
                </tr>
                <tr>
                    <td style="padding: 8px;"><strong>Leave Type</strong></td>
                    <td style="padding: 8px;">{leave_data.get('leave_type', '')}</td>
                </tr>
                <tr style="background-color: #ecf0f1;">
                    <td style="padding: 8px;"><strong>Start Date</strong></td>
                    <td style="padding: 8px;">{leave_data.get('start_date', '')}</td>
                </tr>
                <tr>
                    <td style="padding: 8px;"><strong>End Date</strong></td>
                    <td style="padding: 8px;">{leave_data.get('end_date', '')}</td>
                </tr>
                <tr style="background-color: #ecf0f1;">
                    <td style="padding: 8px;"><strong>Days</strong></td>
                    <td style="padding: 8px;">{leave_data.get('days', 0)}</td>
                </tr>
                <tr>
                    <td style="padding: 8px;"><strong>Reason</strong></td>
                    <td style="padding: 8px;">{leave_data.get('reason', '')}</td>
                </tr>
            </table>
            <p style="margin-top: 20px;">Please log in to the system to approve or reject this request.</p>
            <p style="color: #7f8c8d;">This is an automated message from the HRMS system.</p>
        </body>
        </html>
        """
        return self.send_email(manager_email, subject, body)
    
    def send_leave_status_notification(self, employee_email, leave_data, status):
        """Send notification when leave is approved/rejected"""
        status_text = "Approved" if status == 'approved' else "Rejected"
        status_color = "#27ae60" if status == 'approved' else "#e74c3c"
        
        subject = f"Leave Request {status_text}: {leave_data.get('leave_type', '')}"
        body = f"""
        <html>
        <body style="font-family: Arial, sans-serif;">
            <h2 style="color: {status_color};">Leave Request {status_text}</h2>
            <p>Your leave request has been {status_text.lower()}.</p>
            <table style="border-collapse: collapse; width: 100%;">
                <tr style="background-color: #3498db; color: white;">
                    <th style="padding: 10px; text-align: left;">Field</th>
                    <th style="padding: 10px; text-align: left;">Value</th>
                </tr>
                <tr style="background-color: #ecf0f1;">
                    <td style="padding: 8px;"><strong>Leave Type</strong></td>
                    <td style="padding: 8px;">{leave_data.get('leave_type', '')}</td>
                </tr>
                <tr>
                    <td style="padding: 8px;"><strong>Start Date</strong></td>
                    <td style="padding: 8px;">{leave_data.get('start_date', '')}</td>
                </tr>
                <tr style="background-color: #ecf0f1;">
                    <td style="padding: 8px;"><strong>End Date</strong></td>
                    <td style="padding: 8px;">{leave_data.get('end_date', '')}</td>
                </tr>
                <tr>
                    <td style="padding: 8px;"><strong>Days</strong></td>
                    <td style="padding: 8px;">{leave_data.get('days', 0)}</td>
                </tr>
            </table>
            <p style="margin-top: 20px; color: #7f8c8d;">This is an automated message from the HRMS system.</p>
        </body>
        </html>
        """
        return self.send_email(employee_email, subject, body)
    
    def send_payroll_notification(self, finance_email, month, total_salaries, employee_count):
        """Send notification when payroll is processed"""
        subject = f"Payroll Processed - {month}"
        body = f"""
        <html>
        <body style="font-family: Arial, sans-serif;">
            <h2 style="color: #2c3e50;">Payroll Summary - {month}</h2>
            <table style="border-collapse: collapse; width: 100%;">
                <tr style="background-color: #3498db; color: white;">
                    <th style="padding: 10px; text-align: left;">Metric</th>
                    <th style="padding: 10px; text-align: left;">Value</th>
                </tr>
                <tr style="background-color: #ecf0f1;">
                    <td style="padding: 8px;"><strong>Month</strong></td>
                    <td style="padding: 8px;">{month}</td>
                </tr>
                <tr>
                    <td style="padding: 8px;"><strong>Employees Processed</strong></td>
                    <td style="padding: 8px;">{employee_count}</td>
                </tr>
                <tr style="background-color: #ecf0f1;">
                    <td style="padding: 8px;"><strong>Total Salaries</strong></td>
                    <td style="padding: 8px;">{total_salaries:,.2f}</td>
                </tr>
            </table>
            <p style="margin-top: 20px; color: #7f8c8d;">This is an automated message from the HRMS system.</p>
        </body>
        </html>
        """
        return self.send_email(finance_email, subject, body)
    
    def send_welcome_email(self, employee_email, employee_name):
        """Send welcome email to new employee"""
        subject = "Welcome to the Company!"
        body = f"""
        <html>
        <body style="font-family: Arial, sans-serif;">
            <h2 style="color: #2c3e50;">Welcome aboard, {employee_name}!</h2>
            <p>We are excited to have you as part of our team.</p>
            <p>You have been successfully added to the HRMS system.</p>
            <p>Please contact HR if you have any questions.</p>
            <br>
            <p>Best regards,</p>
            <p><strong>HR Department</strong></p>
        </body>
        </html>
        """
        return self.send_email(employee_email, subject, body)


# Create single instance
email_notifier = EmailNotifier()