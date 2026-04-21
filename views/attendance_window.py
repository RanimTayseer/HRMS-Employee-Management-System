"""
attendance_window.py - Attendance Check-in/Check-out Window
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.attendance import Attendance
from models.employee import Employee


class AttendanceWindow:
    """Attendance Check-in/Check-out Window"""
    
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame
        self.attendance_model = Attendance()
        self.employee_model = Employee()
        self.setup_ui()
        self.load_data()
    
    def setup_ui(self):
        # Clear previous content
        for widget in self.parent_frame.winfo_children():
            widget.destroy()
        
        # Title
        title = tk.Label(
            self.parent_frame,
            text="⏰ Attendance Check-in / Check-out",
            font=("Arial", 24, "bold"),
            bg="white",
            fg="#1e5799"
        )
        title.pack(pady=20)
        
        # Top control frame
        control_frame = tk.Frame(self.parent_frame, bg="white")
        control_frame.pack(fill='x', padx=20, pady=10)
        
        # Employee selection
        tk.Label(
            control_frame,
            text="Select Employee:",
            font=("Arial", 11),
            bg="white"
        ).pack(side='left', padx=5)
        
        self.employee_combo = ttk.Combobox(control_frame, font=("Arial", 11), width=30)
        self.employee_combo.pack(side='left', padx=5)
        
        # Check-in button
        check_in_btn = tk.Button(
            control_frame,
            text="✅ Check In",
            font=("Arial", 11, "bold"),
            bg="#2ecc71",
            fg="white",
            padx=15,
            pady=8,
            cursor="hand2",
            command=self.check_in
        )
        check_in_btn.pack(side='left', padx=5)
        
        # Check-out button
        check_out_btn = tk.Button(
            control_frame,
            text="❌ Check Out",
            font=("Arial", 11, "bold"),
            bg="#e74c3c",
            fg="white",
            padx=15,
            pady=8,
            cursor="hand2",
            command=self.check_out
        )
        check_out_btn.pack(side='left', padx=5)
        
        # Refresh button
        refresh_btn = tk.Button(
            control_frame,
            text="🔄 Refresh",
            font=("Arial", 11),
            bg="#3498db",
            fg="white",
            padx=15,
            pady=8,
            cursor="hand2",
            command=self.load_data
        )
        refresh_btn.pack(side='left', padx=5)
        
        # Display date
        today = datetime.now().strftime("%Y-%m-%d")
        tk.Label(
            control_frame,
            text=f"📅 Date: {today}",
            font=("Arial", 11),
            bg="white",
            fg="#1e5799"
        ).pack(side='right', padx=5)
        
        # Load employee list
        self.load_employees()
        
        # Table frame
        table_frame = tk.Frame(self.parent_frame, bg="white")
        table_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Create table
        columns = ('ID', 'Employee', 'Date', 'Check In', 'Check Out', 'Status')
        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=20)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)
        
        self.tree.column('Employee', width=180)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Status message
        self.status_label = tk.Label(
            self.parent_frame,
            text="",
            font=("Arial", 10),
            bg="white",
            fg="gray"
        )
        self.status_label.pack(pady=5)
    
    def load_employees(self):
        """Load employee list"""
        employees = self.employee_model.get_active()
        employee_list = [f"{e['employee_id']} - {e['full_name']}" for e in employees]
        self.employee_combo['values'] = employee_list
        if employee_list:
            self.employee_combo.set(employee_list[0])
    
    def get_selected_employee_id(self):
        """Get selected employee ID"""
        selection = self.employee_combo.get()
        if selection:
            try:
                return int(selection.split(' - ')[0])
            except:
                return None
        return None
    
    def check_in(self):
        """Check-in employee"""
        employee_id = self.get_selected_employee_id()
        if not employee_id:
            messagebox.showerror("Error", "Please select an employee")
            return
        
        result, message = self.attendance_model.check_in(employee_id)
        if result:
            messagebox.showinfo("Success", message)
            self.load_data()
        else:
            messagebox.showerror("Error", message)
    
    def check_out(self):
        """Check-out employee"""
        employee_id = self.get_selected_employee_id()
        if not employee_id:
            messagebox.showerror("Error", "Please select an employee")
            return
        
        result, message = self.attendance_model.check_out(employee_id)
        if result:
            messagebox.showinfo("Success", message)
            self.load_data()
        else:
            messagebox.showerror("Error", message)
    
    def load_data(self):
        """Load attendance data to table"""
        # Clear old data
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Get today's attendance
        attendance = self.attendance_model.get_today_attendance()
        
        if not attendance:
            self.status_label.config(text="⚠️ No attendance records for today")
            return
        
        self.status_label.config(text=f"📊 Today's records: {len(attendance)}")
        
        for att in attendance:
            self.tree.insert('', 'end', values=(
                att.get('attendance_id', ''),
                att.get('full_name', ''),
                att.get('date', ''),
                att.get('check_in', ''),
                att.get('check_out', ''),
                att.get('status', '')
            ))