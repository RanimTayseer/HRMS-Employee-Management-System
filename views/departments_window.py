"""
departments_window.py - Departments Management Window
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.department import Department


class DepartmentsWindow:
    """Departments Management Window"""
    
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame
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
            text="🏢 Departments Management",
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
            text="➕ Add New Department",
            font=("Arial", 11),
            bg="#2ecc71",
            fg="white",
            padx=15,
            pady=8,
            cursor="hand2",
            command=self.add_department
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
            command=self.edit_department
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
            command=self.delete_department
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
        
        # Table frame
        table_frame = tk.Frame(self.parent_frame, bg="white")
        table_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Create table
        columns = ('ID', 'Dept Code', 'Dept Name', 'Description', 'Employees')
        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=20)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)
        
        self.tree.column('Dept Name', width=180)
        self.tree.column('Description', width=250)
        
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
        self.tree.bind('<Double-Button-1>', lambda e: self.edit_department())
    
    def load_data(self):
        """Load data into table"""
        # Clear old data
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        departments = self.department_model.get_all()
        
        if not departments:
            self.status_label.config(text="⚠️ No departments found")
            return
        
        self.status_label.config(text=f"📊 Total Departments: {len(departments)}")
        
        for dept in departments:
            self.tree.insert('', 'end', values=(
                dept.get('department_id', ''),
                dept.get('department_code', ''),
                dept.get('department_name', ''),
                (dept.get('description', '') or '')[:50],
                dept.get('employee_count', 0)
            ))
    
    def get_selected_department(self):
        """Get selected department"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a department first")
            return None
        values = self.tree.item(selected[0])['values']
        return values[0]  # department_id
    
    def add_department(self):
        """Add new department"""
        self.open_department_form()
    
    def edit_department(self):
        """Edit department"""
        department_id = self.get_selected_department()
        if department_id:
            self.open_department_form(department_id)
    
    def delete_department(self):
        """Delete department"""
        department_id = self.get_selected_department()
        if not department_id:
            return
        
        # Check if department has employees
        departments = self.department_model.get_all()
        for dept in departments:
            if dept.get('department_id') == department_id and dept.get('employee_count', 0) > 0:
                messagebox.showerror("Error", "Cannot delete this department because it has employees")
                return
        
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this department?"):
            self.department_model.delete(department_id)
            messagebox.showinfo("Success", "Department deleted successfully")
            self.load_data()
    
    def open_department_form(self, department_id=None):
        """Open add/edit department form"""
        window = tk.Toplevel(self.parent_frame)
        window.title("Add New Department" if not department_id else "Edit Department")
        window.geometry("500x450")
        window.resizable(False, False)
        window.configure(bg="#f0f4f8")
        
        # Title
        tk.Label(
            window,
            text="➕ Add New Department" if not department_id else "✏️ Edit Department",
            font=("Arial", 18, "bold"),
            bg="#f0f4f8",
            fg="#1e5799"
        ).pack(pady=20)
        
        # Form frame
        form_frame = tk.Frame(window, bg="white", relief=tk.RAISED)
        form_frame.pack(fill='both', expand=True, padx=30, pady=10)
        
        # Department Code
        frame1 = tk.Frame(form_frame, bg="white")
        frame1.pack(fill='x', padx=20, pady=10)
        
        tk.Label(
            frame1,
            text="Department Code:",
            font=("Arial", 11),
            bg="white",
            width=15,
            anchor='w'
        ).pack(side='left')
        
        code_entry = tk.Entry(frame1, font=("Arial", 11), width=30)
        code_entry.pack(side='left', padx=10)
        
        # Department Name
        frame2 = tk.Frame(form_frame, bg="white")
        frame2.pack(fill='x', padx=20, pady=10)
        
        tk.Label(
            frame2,
            text="Department Name:",
            font=("Arial", 11),
            bg="white",
            width=15,
            anchor='w'
        ).pack(side='left')
        
        name_entry = tk.Entry(frame2, font=("Arial", 11), width=30)
        name_entry.pack(side='left', padx=10)
        
        # Description
        frame3 = tk.Frame(form_frame, bg="white")
        frame3.pack(fill='x', padx=20, pady=10)
        
        tk.Label(
            frame3,
            text="Description:",
            font=("Arial", 11),
            bg="white",
            width=15,
            anchor='w'
        ).pack(side='left')
        
        desc_text = tk.Text(frame3, font=("Arial", 11), height=5, width=30)
        desc_text.pack(side='left', padx=10)
        
        # If editing, load data
        if department_id:
            dept = self.department_model.get_by_id(department_id)
            if dept:
                code_entry.insert(0, dept.get('department_code', ''))
                name_entry.insert(0, dept.get('department_name', ''))
                desc_text.insert('1.0', dept.get('description', ''))
        
        # Save and Cancel buttons
        def save():
            code = code_entry.get().strip()
            name = name_entry.get().strip()
            description = desc_text.get('1.0', 'end').strip()
            
            if not code or not name:
                messagebox.showerror("Error", "Please fill all required fields")
                return
            
            if department_id:
                # Update
                self.department_model.update(department_id, (code, name, description))
                messagebox.showinfo("Success", "Department updated successfully")
            else:
                # Add new
                self.department_model.add((code, name, description))
                messagebox.showinfo("Success", "Department added successfully")
            
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