"""
employees_window.py - Employees Management Window
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.employee import Employee
from models.department import Department


class EmployeesWindow:
    """Employees Management Window"""
    
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame
        self.employee_model = Employee()
        self.department_model = Department()
        self.setup_ui()
        self.load_data()
    
    def setup_ui(self):
        # Clear previous content
        for widget in self.parent_frame.winfo_children():
            widget.destroy()
        
        # Title
        title = tk.Label(
            self.parent_frame,
            text="👥 Employees Management",
            font=("Arial", 24, "bold"),
            bg="white",
            fg="#1e5799"
        )
        title.pack(pady=20)
        
        # Buttons frame
        buttons_frame = tk.Frame(self.parent_frame, bg="white")
        buttons_frame.pack(fill='x', padx=20, pady=10)
        
        # Add button
        add_btn = tk.Button(
            buttons_frame,
            text="➕ Add New Employee",
            font=("Arial", 11),
            bg="#2ecc71",
            fg="white",
            padx=15,
            pady=8,
            cursor="hand2",
            command=self.add_employee
        )
        add_btn.pack(side='left', padx=5)
        
        # Edit button
        edit_btn = tk.Button(
            buttons_frame,
            text="✏️ Edit",
            font=("Arial", 11),
            bg="#3498db",
            fg="white",
            padx=15,
            pady=8,
            cursor="hand2",
            command=self.edit_employee
        )
        edit_btn.pack(side='left', padx=5)
        
        # Delete button
        delete_btn = tk.Button(
            buttons_frame,
            text="🗑️ Delete",
            font=("Arial", 11),
            bg="#e74c3c",
            fg="white",
            padx=15,
            pady=8,
            cursor="hand2",
            command=self.delete_employee
        )
        delete_btn.pack(side='left', padx=5)
        
        # Refresh button
        refresh_btn = tk.Button(
            buttons_frame,
            text="🔄 Refresh",
            font=("Arial", 11),
            bg="#95a5a6",
            fg="white",
            padx=15,
            pady=8,
            cursor="hand2",
            command=self.load_data
        )
        refresh_btn.pack(side='left', padx=5)
        
        # Search frame
        search_frame = tk.Frame(self.parent_frame, bg="white")
        search_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(
            search_frame,
            text="🔍 Search:",
            font=("Arial", 11),
            bg="white"
        ).pack(side='left', padx=5)
        
        self.search_entry = tk.Entry(
            search_frame,
            font=("Arial", 11),
            width=30
        )
        self.search_entry.pack(side='left', padx=5)
        
        search_btn = tk.Button(
            search_frame,
            text="Search",
            font=("Arial", 10),
            bg="#1e5799",
            fg="white",
            padx=10,
            pady=5,
            cursor="hand2",
            command=self.search
        )
        search_btn.pack(side='left', padx=5)
        
        # Table frame
        table_frame = tk.Frame(self.parent_frame, bg="white")
        table_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Create table
        columns = ('ID', 'Employee ID', 'Name', 'Email', 'Department', 'Position', 'Salary', 'Status')
        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=20)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)
        
        self.tree.column('Name', width=150)
        self.tree.column('Email', width=160)
        
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
        
        # Double-click to edit
        self.tree.bind('<Double-Button-1>', lambda e: self.edit_employee())
    
    def load_data(self):
        """Load data into table"""
        # Clear old data
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        employees = self.employee_model.get_all()
        
        if not employees:
            self.status_label.config(text="⚠️ No employees found")
            return
        
        self.status_label.config(text=f"📊 Total Employees: {len(employees)}")
        
        for emp in employees:
            self.tree.insert('', 'end', values=(
                emp.get('employee_id', ''),
                emp.get('employee_number', ''),
                emp.get('full_name', ''),
                emp.get('email', ''),
                emp.get('department_name', ''),
                emp.get('position', ''),
                f"{emp.get('basic_salary', 0):,.2f}",
                emp.get('status', '')
            ))
    
    def search(self):
        """Search employees"""
        keyword = self.search_entry.get().strip()
        
        if not keyword:
            self.load_data()
            return
        
        # Clear old data
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        employees = self.employee_model.search(keyword)
        
        if not employees:
            self.status_label.config(text=f"⚠️ No results found for '{keyword}'")
            return
        
        self.status_label.config(text=f"📊 Search results: {len(employees)}")
        
        for emp in employees:
            self.tree.insert('', 'end', values=(
                emp.get('employee_id', ''),
                emp.get('employee_number', ''),
                emp.get('full_name', ''),
                emp.get('email', ''),
                emp.get('department_name', ''),
                emp.get('position', ''),
                f"{emp.get('basic_salary', 0):,.2f}",
                emp.get('status', '')
            ))
    
    def get_selected_employee(self):
        """Get selected employee"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an employee first")
            return None
        
        values = self.tree.item(selected[0])['values']
        return values[0]  # employee_id
    
    def add_employee(self):
        """Add new employee"""
        self.open_employee_form()
    
    def edit_employee(self):
        """Edit employee"""
        employee_id = self.get_selected_employee()
        if employee_id:
            self.open_employee_form(employee_id)
    
    def delete_employee(self):
        """Delete employee"""
        employee_id = self.get_selected_employee()
        if not employee_id:
            return
        
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this employee?"):
            self.employee_model.delete(employee_id)
            messagebox.showinfo("Success", "Employee deleted successfully")
            self.load_data()
    
    def open_employee_form(self, employee_id=None):
        """Open add/edit employee form"""
        window = tk.Toplevel(self.parent_frame)
        window.title("Add New Employee" if not employee_id else "Edit Employee")
        window.geometry("550x600")
        window.resizable(False, False)
        window.configure(bg="#f0f4f8")
        
        # Title
        tk.Label(
            window,
            text="➕ Add New Employee" if not employee_id else "✏️ Edit Employee",
            font=("Arial", 18, "bold"),
            bg="#f0f4f8",
            fg="#1e5799"
        ).pack(pady=20)
        
        # Form frame
        form_frame = tk.Frame(window, bg="white", relief=tk.RAISED)
        form_frame.pack(fill='both', expand=True, padx=30, pady=10)
        
        # Input fields
        entries = {}
        
        fields = [
            ("Full Name:", "full_name"),
            ("Email:", "email"),
            ("Phone:", "phone"),
            ("Address:", "address"),
            ("Position:", "position"),
            ("Basic Salary:", "basic_salary"),
            ("Hire Date (YYYY-MM-DD):", "hire_date"),
        ]
        
        for label, key in fields:
            frame = tk.Frame(form_frame, bg="white")
            frame.pack(fill='x', padx=20, pady=8)
            
            tk.Label(
                frame,
                text=label,
                font=("Arial", 11),
                bg="white",
                width=20,
                anchor='w'
            ).pack(side='left')
            
            entry = tk.Entry(frame, font=("Arial", 11), width=30)
            entry.pack(side='left', padx=10)
            entries[key] = entry
        
        # Department dropdown
        frame = tk.Frame(form_frame, bg="white")
        frame.pack(fill='x', padx=20, pady=8)
        
        tk.Label(
            frame,
            text="Department:",
            font=("Arial", 11),
            bg="white",
            width=20,
            anchor='w'
        ).pack(side='left')
        
        department_combo = ttk.Combobox(frame, font=("Arial", 11), width=28)
        department_combo.pack(side='left', padx=10)
        
        # Load departments
        departments = self.department_model.get_all()
        department_dict = {d['department_name']: d['department_id'] for d in departments}
        department_combo['values'] = list(department_dict.keys())
        if department_combo['values']:
            department_combo.set(department_combo['values'][0])
        
        # If editing, load data
        if employee_id:
            emp = self.employee_model.get_by_id(employee_id)
            if emp:
                entries['full_name'].insert(0, emp.get('full_name', ''))
                entries['email'].insert(0, emp.get('email', ''))
                entries['phone'].insert(0, emp.get('phone', ''))
                entries['address'].insert(0, emp.get('address', ''))
                entries['position'].insert(0, emp.get('position', ''))
                entries['basic_salary'].insert(0, emp.get('basic_salary', ''))
                entries['hire_date'].insert(0, emp.get('hire_date', ''))
                
                # Set department
                for name, dept_id in department_dict.items():
                    if dept_id == emp.get('department_id'):
                        department_combo.set(name)
                        break
        
        # Save and Cancel buttons
        def save():
            full_name = entries['full_name'].get().strip()
            email = entries['email'].get().strip()
            phone = entries['phone'].get().strip()
            address = entries['address'].get().strip()
            position = entries['position'].get().strip()
            
            try:
                basic_salary = float(entries['basic_salary'].get() or 0)
            except:
                basic_salary = 0
            
            department_id = department_dict.get(department_combo.get(), 1)
            hire_date = entries['hire_date'].get().strip()
            
            if not full_name or not email or not position or not hire_date:
                messagebox.showerror("Error", "Please fill all required fields")
                return
            
            if employee_id:
                # Update
                self.employee_model.update(employee_id, (full_name, email, phone, address, department_id, position, basic_salary))
                messagebox.showinfo("Success", "Employee updated successfully")
            else:
                # Add new
                emp_number = self.employee_model.generate_employee_number()
                self.employee_model.add((emp_number, full_name, email, phone, address, department_id, position, basic_salary, hire_date))
                messagebox.showinfo("Success", "Employee added successfully")
            
            window.destroy()
            self.load_data()
        
        buttons_frame = tk.Frame(form_frame, bg="white")
        buttons_frame.pack(pady=20)
        
        tk.Button(
            buttons_frame,
            text="💾 Save",
            font=("Arial", 11, "bold"),
            bg="#2ecc71",
            fg="white",
            padx=30,
            pady=8,
            cursor="hand2",
            command=save
        ).pack(side='left', padx=10)
        
        tk.Button(
            buttons_frame,
            text="❌ Cancel",
            font=("Arial", 11),
            bg="#95a5a6",
            fg="white",
            padx=30,
            pady=8,
            cursor="hand2",
            command=window.destroy
        ).pack(side='left', padx=10)
        
        window.grab_set()
        window.wait_window()