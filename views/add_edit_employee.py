"""
add_edit_employee.py - Add/Edit Employee Window
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.employee import Employee
from models.department import Department


class AddEditEmployee:
    """Add or Edit Employee Window"""
    
    def __init__(self, parent, employee_id=None, callback=None):
        self.parent = parent
        self.employee_id = employee_id
        self.callback = callback
        self.employee_model = Employee()
        self.department_model = Department()
        
        self.window = tk.Toplevel(parent)
        self.window.title("Add New Employee" if not employee_id else "Edit Employee")
        self.window.geometry("600x700")
        self.window.resizable(False, False)
        self.window.configure(bg="#f0f4f8")
        
        self.setup_ui()
        
        if employee_id:
            self.load_employee_data()
    
    def setup_ui(self):
        # Title
        title = tk.Label(
            self.window,
            text="➕ Add New Employee" if not self.employee_id else "✏️ Edit Employee",
            font=("Arial", 18, "bold"),
            bg="#f0f4f8",
            fg="#1e5799"
        )
        title.pack(pady=20)
        
        # Form frame
        form_frame = tk.Frame(self.window, bg="white", relief=tk.RAISED, bd=0)
        form_frame.pack(fill='both', expand=True, padx=30, pady=10)
        
        # Input fields
        fields = [
            ("Full Name:", "full_name"),
            ("Email:", "email"),
            ("Phone:", "phone"),
            ("Address:", "address"),
            ("Birth Date (YYYY-MM-DD):", "birth_date"),
            ("National ID:", "national_id"),
            ("Position:", "position"),
            ("Basic Salary:", "basic_salary"),
            ("Housing Allowance:", "housing_allowance"),
            ("Transport Allowance:", "transport_allowance"),
            ("Hire Date (YYYY-MM-DD):", "hire_date"),
        ]
        
        self.entries = {}
        
        for i, (label, key) in enumerate(fields):
            frame = tk.Frame(form_frame, bg="white")
            frame.pack(fill='x', padx=20, pady=8)
            
            tk.Label(
                frame,
                text=label,
                font=("Arial", 10),
                bg="white",
                width=20,
                anchor='w'
            ).pack(side='left')
            
            entry = tk.Entry(frame, font=("Arial", 10), width=35)
            entry.pack(side='left', padx=10)
            self.entries[key] = entry
        
        # Department dropdown
        frame = tk.Frame(form_frame, bg="white")
        frame.pack(fill='x', padx=20, pady=8)
        
        tk.Label(
            frame,
            text="Department:",
            font=("Arial", 10),
            bg="white",
            width=20,
            anchor='w'
        ).pack(side='left')
        
        self.department_combo = ttk.Combobox(frame, font=("Arial", 10), width=33)
        self.department_combo.pack(side='left', padx=10)
        
        # Load departments
        departments = self.department_model.get_all()
        self.departments_list = {d['department_name']: d['department_id'] for d in departments}
        self.department_combo['values'] = list(self.departments_list.keys())
        
        # Employment type dropdown
        frame = tk.Frame(form_frame, bg="white")
        frame.pack(fill='x', padx=20, pady=8)
        
        tk.Label(
            frame,
            text="Employment Type:",
            font=("Arial", 10),
            bg="white",
            width=20,
            anchor='w'
        ).pack(side='left')
        
        self.employment_combo = ttk.Combobox(
            frame,
            font=("Arial", 10),
            width=33,
            values=['full_time', 'part_time', 'contract', 'intern']
        )
        self.employment_combo.pack(side='left', padx=10)
        self.employment_combo.set('full_time')
        
        # Buttons
        buttons_frame = tk.Frame(form_frame, bg="white")
        buttons_frame.pack(pady=20)
        
        save_btn = tk.Button(
            buttons_frame,
            text="💾 Save",
            font=("Arial", 11, "bold"),
            bg="#2ecc71",
            fg="white",
            padx=30,
            pady=8,
            cursor="hand2",
            command=self.save
        )
        save_btn.pack(side='left', padx=10)
        
        cancel_btn = tk.Button(
            buttons_frame,
            text="❌ Cancel",
            font=("Arial", 11),
            bg="#95a5a6",
            fg="white",
            padx=30,
            pady=8,
            cursor="hand2",
            command=self.window.destroy
        )
        cancel_btn.pack(side='left', padx=10)
    
    def load_employee_data(self):
        """Load employee data for editing"""
        employee = self.employee_model.get_by_id(self.employee_id)
        
        if employee:
            self.entries['full_name'].insert(0, employee.get('full_name', ''))
            self.entries['email'].insert(0, employee.get('email', ''))
            self.entries['phone'].insert(0, employee.get('phone', ''))
            self.entries['address'].insert(0, employee.get('address', ''))
            self.entries['birth_date'].insert(0, employee.get('birth_date', ''))
            self.entries['national_id'].insert(0, employee.get('national_id', ''))
            self.entries['position'].insert(0, employee.get('position', ''))
            self.entries['basic_salary'].insert(0, employee.get('basic_salary', ''))
            self.entries['housing_allowance'].insert(0, employee.get('housing_allowance', ''))
            self.entries['transport_allowance'].insert(0, employee.get('transport_allowance', ''))
            self.entries['hire_date'].insert(0, employee.get('hire_date', ''))
            
            # Set department
            dept_name = None
            for name, dept_id in self.departments_list.items():
                if dept_id == employee.get('department_id'):
                    dept_name = name
                    break
            if dept_name:
                self.department_combo.set(dept_name)
            
            self.employment_combo.set(employee.get('employment_type', 'full_time'))
    
    def save(self):
        """Save data"""
        # Collect data
        data = (
            self.entries['full_name'].get().strip(),
            self.entries['email'].get().strip(),
            self.entries['phone'].get().strip(),
            self.entries['address'].get().strip(),
            self.entries['birth_date'].get().strip(),
            self.entries['national_id'].get().strip(),
            self.departments_list.get(self.department_combo.get(), None),
            self.entries['position'].get().strip(),
            self.employment_combo.get(),
            float(self.entries['basic_salary'].get() or 0),
            float(self.entries['housing_allowance'].get() or 0),
            float(self.entries['transport_allowance'].get() or 0),
            self.entries['hire_date'].get().strip(),
            None,  # contract_end_date
            'active'
        )
        
        # Validate required fields
        if not data[0] or not data[1] or not data[8] or not data[12]:
            messagebox.showerror("Error", "Please fill all required fields")
            return
        
        if self.employee_id:
            # Update
            update_data = (
                data[0], data[1], data[2], data[3],
                data[6], data[7], data[9], data[10], data[11]
            )
            self.employee_model.update(self.employee_id, update_data)
            messagebox.showinfo("Success", "Employee updated successfully")
        else:
            # Add new
            emp_number = self.employee_model.generate_employee_number()
            full_data = (emp_number,) + data
            self.employee_model.add(full_data)
            messagebox.showinfo("Success", "Employee added successfully")
        
        self.window.destroy()
        if self.callback:
            self.callback()
    
    def show(self):
        self.window.grab_set()
        self.window.wait_window()