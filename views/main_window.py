"""
main_window.py - Main Application Window
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.session_manager import session
from database.db_manager import db


class MainWindow:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Employee Management System")
        self.window.geometry("1200x700")
        self.window.state('zoomed')
        
        self.colors = {
            'primary': '#1e5799',
            'secondary': '#3498db',
            'success': '#2ecc71',
            'danger': '#e74c3c',
            'warning': '#f39c12',
            'light': '#ecf0f1',
            'dark': '#2c3e50',
            'white': '#ffffff'
        }
        
        self.setup_ui()
        self.show_dashboard()
        
    def setup_ui(self):
        # Header frame
        header = tk.Frame(self.window, bg=self.colors['primary'], height=60)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        tk.Label(
            header,
            text="Employee Management System",
            font=("Arial", 20, "bold"),
            bg=self.colors['primary'],
            fg='white'
        ).pack(side='left', padx=20, pady=10)
        
        user_text = f"👤 {session.current_user.get('username', '')} | {session.current_user.get('role', 'employee')}"
        tk.Label(
            header,
            text=user_text,
            font=("Arial", 11),
            bg=self.colors['primary'],
            fg='white'
        ).pack(side='right', padx=20, pady=10)
        
        # Sidebar menu
        sidebar = tk.Frame(self.window, bg=self.colors['light'], width=220)
        sidebar.pack(side='left', fill='y')
        sidebar.pack_propagate(False)
        
        menu_items = [
            ("🏠 Dashboard", self.show_dashboard),
            ("👥 Employees", self.show_employees),
            ("🏢 Departments", self.show_departments),
            ("⏰ Attendance", self.show_attendance),
            ("📅 Leaves", self.show_leaves),
            ("💰 Payroll", self.show_payroll),
            ("📊 Reports", self.show_reports),
            ("⚙️ Settings", self.show_settings),
            ("🚪 Logout", self.logout)
        ]
        
        for text, command in menu_items:
            btn = tk.Button(
                sidebar,
                text=text,
                font=("Arial", 11),
                bg=self.colors['light'],
                fg=self.colors['dark'],
                bd=0,
                anchor='w',
                padx=20,
                pady=12,
                cursor="hand2",
                command=command
            )
            btn.pack(fill='x')
        
        # Content area
        self.content_frame = tk.Frame(self.window, bg=self.colors['white'])
        self.content_frame.pack(side='left', fill='both', expand=True)
    
    def clear_content(self):
        """Clear main content area"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def show_dashboard(self):
        """Show dashboard"""
        self.clear_content()
        
        tk.Label(
            self.content_frame,
            text="🏠 Dashboard",
            font=("Arial", 24, "bold"),
            bg=self.colors['white'],
            fg=self.colors['primary']
        ).pack(pady=20)
        
        # Quick statistics
        stats_frame = tk.Frame(self.content_frame, bg=self.colors['white'])
        stats_frame.pack(pady=20, padx=40, fill='x')
        
        employees_count = db.get_table_count('employees')
        departments_count = db.get_table_count('departments')
        
        stats = [
            ("👥 Total Employees", employees_count, self.colors['secondary']),
            ("🏢 Total Departments", departments_count, self.colors['success']),
        ]
        
        for i, (label, value, color) in enumerate(stats):
            card = tk.Frame(stats_frame, bg=color, relief=tk.RAISED)
            card.grid(row=0, column=i, padx=10, pady=10, sticky='nsew')
            stats_frame.grid_columnconfigure(i, weight=1)
            
            tk.Label(card, text=label, font=("Arial", 14), bg=color, fg='white').pack(pady=(20, 5))
            tk.Label(card, text=str(value), font=("Arial", 32, "bold"), bg=color, fg='white').pack(pady=(5, 20))
        
        # Recent Activities Section
        try:
            from models.activity import ActivityModel
            activity_model = ActivityModel()
            activities = activity_model.get_recent_activities(10)
            
            activities_frame = tk.LabelFrame(
                self.content_frame,
                text="📊 Recent Activities",
                font=("Arial", 12, "bold"),
                bg="white",
                fg="#1e5799"
            )
            activities_frame.pack(fill='both', expand=True, padx=40, pady=20)
            
            if activities:
                for activity in activities:
                    time_str = activity.get('created_at', '')[:16]
                    username = activity.get('username', 'System')
                    description = activity.get('description', '')
                    
                    text = f"• [{time_str}] {username}: {description}"
                    tk.Label(
                        activities_frame,
                        text=text,
                        font=("Arial", 10),
                        bg="white",
                        fg="gray",
                        anchor='w'
                    ).pack(fill='x', padx=15, pady=5)
            else:
                tk.Label(
                    activities_frame,
                    text="📭 No recent activities yet. Start using the system to see activities here!",
                    font=("Arial", 11),
                    bg="white",
                    fg="gray",
                    pady=20
                ).pack()
        except Exception as e:
            # If activity table doesn't exist yet, show this message
            activities_frame = tk.LabelFrame(
                self.content_frame,
                text="📊 Recent Activities",
                font=("Arial", 12, "bold"),
                bg="white",
                fg="#1e5799"
            )
            activities_frame.pack(fill='both', expand=True, padx=40, pady=20)
            tk.Label(
                activities_frame,
                text="📭 Activities feature coming soon. Add the activities table to enable this feature.",
                font=("Arial", 11),
                bg="white",
                fg="gray",
                pady=20
            ).pack()
    
    def show_employees(self):
        """Show employees management page"""
        self.clear_content()
        from views.employees_window import EmployeesWindow
        EmployeesWindow(self.content_frame)

    def show_departments(self):
        """Show departments management page"""
        self.clear_content()
        from views.departments_window import DepartmentsWindow
        DepartmentsWindow(self.content_frame)
    
    def show_attendance(self):
        """Show attendance page"""
        self.clear_content()
        from views.attendance_window import AttendanceWindow
        AttendanceWindow(self.content_frame)
    
    def show_leaves(self):
        """Show leaves management page"""
        self.clear_content()
        from views.leaves_window import LeavesWindow
        LeavesWindow(self.content_frame)

    def show_payroll(self):
        """Show payroll management page"""
        self.clear_content()
        from views.payroll_window import PayrollWindow
        PayrollWindow(self.content_frame)
    
    def show_reports(self):
        """Show reports page"""
        self.clear_content()
        from views.reports_window import ReportsWindow
        ReportsWindow(self.content_frame)
    
    def show_settings(self):
        """Show settings page"""
        self.clear_content()
        from views.settings_window import SettingsWindow
        SettingsWindow(self.content_frame)
    
    def logout(self):
        """Logout user"""
        if messagebox.askyesno("Confirm", "Are you sure you want to logout?"):
            session.logout()
            self.window.destroy()
            from views.login_window import LoginWindow
            LoginWindow().run()
    
    def run(self):
        """Run the window"""
        self.window.mainloop()