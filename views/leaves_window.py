"""
leaves_window.py - Leaves Management Window
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.leave import LeaveModel
from models.employee import Employee


class LeavesWindow:
    """Leaves Management Window"""
    
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame
        self.leave_model = LeaveModel()
        self.employee_model = Employee()
        self.setup_ui()
        self.load_data()

    def setup_ui(self):
        # Clear previous content
        for widget in self.parent_frame.winfo_children():
            widget.destroy()

        # Title
        tk.Label(
            self.parent_frame,
            text="📅 Leaves Management",
            font=("Arial", 24, "bold"),
            bg="white",
            fg="#1e5799"
        ).pack(pady=20)

        # Buttons frame
        btn_frame = tk.Frame(self.parent_frame, bg="white")
        btn_frame.pack(pady=10)

        # New Leave Request button
        tk.Button(
            btn_frame,
            text="➕ New Leave Request",
            bg="#2ecc71",
            fg="white",
            font=("Arial", 11),
            padx=15,
            pady=5,
            cursor="hand2",
            command=self.request_leave
        ).pack(side='left', padx=5)

        # Approve button
        tk.Button(
            btn_frame,
            text="✅ Approve",
            bg="#3498db",
            fg="white",
            font=("Arial", 11),
            padx=15,
            pady=5,
            cursor="hand2",
            command=self.approve_leave
        ).pack(side='left', padx=5)

        # Reject button
        tk.Button(
            btn_frame,
            text="❌ Reject",
            bg="#e74c3c",
            fg="white",
            font=("Arial", 11),
            padx=15,
            pady=5,
            cursor="hand2",
            command=self.reject_leave
        ).pack(side='left', padx=5)

        # Refresh button
        tk.Button(
            btn_frame,
            text="🔄 Refresh",
            bg="#95a5a6",
            fg="white",
            font=("Arial", 11),
            padx=15,
            pady=5,
            cursor="hand2",
            command=self.load_data
        ).pack(side='left', padx=5)

        # Filter frame
        filter_frame = tk.Frame(self.parent_frame, bg="white")
        filter_frame.pack(fill='x', padx=20, pady=5)

        tk.Label(
            filter_frame,
            text="Show:",
            font=("Arial", 10),
            bg="white"
        ).pack(side='left', padx=5)

        self.filter_var = tk.StringVar(value="pending")
        filters = [("Pending", "pending"), ("Approved", "approved"), ("Rejected", "rejected"), ("All", "all")]

        for text, value in filters:
            rb = tk.Radiobutton(
                filter_frame,
                text=text,
                variable=self.filter_var,
                value=value,
                font=("Arial", 10),
                bg="white",
                command=self.load_data
            )
            rb.pack(side='left', padx=5)

        # Table frame
        table_frame = tk.Frame(self.parent_frame, bg="white")
        table_frame.pack(fill='both', expand=True, padx=20, pady=10)

        # Create table
        columns = ('ID', 'Employee', 'Department', 'Type', 'Start Date', 'End Date', 'Days', 'Reason', 'Status')
        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=20)

        widths = [50, 150, 100, 100, 100, 100, 70, 200, 100]
        for col, width in zip(columns, widths):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width)

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

    def load_data(self):
        """Load data into table"""
        for item in self.tree.get_children():
            self.tree.delete(item)

        filter_value = self.filter_var.get()

        if filter_value == "all":
            leaves = self.leave_model.get_all()
        else:
            query = """
            SELECT l.*, e.full_name, e.employee_number, d.department_name
            FROM leaves l
            JOIN employees e ON l.employee_id = e.employee_id
            LEFT JOIN departments d ON e.department_id = d.department_id
            WHERE l.status = ?
            ORDER BY l.created_at DESC
            """
            leaves = self.leave_model.db.execute_query(query, (filter_value,))

        if not leaves:
            self.status_label.config(text="⚠️ No leave requests found")
            return

        self.status_label.config(text=f"📊 Total Leaves: {len(leaves)}")

        status_map = {
            'pending': '⏳ Pending',
            'approved': '✅ Approved',
            'rejected': '❌ Rejected'
        }

        for leave in leaves:
            self.tree.insert('', 'end', values=(
                leave.get('leave_id', ''),
                leave.get('full_name', ''),
                leave.get('department_name', ''),
                leave.get('leave_type', ''),
                leave.get('start_date', ''),
                leave.get('end_date', ''),
                leave.get('days_count', ''),
                (leave.get('reason', '') or '')[:50],
                status_map.get(leave.get('status', ''), leave.get('status', ''))
            ))

    def get_selected(self):
        """Get selected leave ID"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a leave request")
            return None
        return self.tree.item(selected[0])['values'][0]

    def request_leave(self):
        """Open new leave request window"""
        window = tk.Toplevel(self.parent_frame)
        window.title("New Leave Request")
        window.geometry("500x550")
        window.resizable(False, False)
        window.configure(bg="#f0f4f8")

        tk.Label(
            window,
            text="➕ New Leave Request",
            font=("Arial", 18, "bold"),
            bg="#f0f4f8",
            fg="#1e5799"
        ).pack(pady=20)

        form_frame = tk.Frame(window, bg="white", relief=tk.RAISED)
        form_frame.pack(fill='both', expand=True, padx=30, pady=10)

        # Employee selection
        frame1 = tk.Frame(form_frame, bg="white")
        frame1.pack(fill='x', padx=20, pady=10)

        tk.Label(
            frame1,
            text="Employee:",
            font=("Arial", 11),
            bg="white",
            width=15,
            anchor='w'
        ).pack(side='left')

        employee_combo = ttk.Combobox(frame1, font=("Arial", 11), width=30)
        employee_combo.pack(side='left', padx=10)

        # Load employee list
        employees = self.employee_model.get_active()
        employee_dict = {f"{e['employee_id']} - {e['full_name']}": e['employee_id'] for e in employees}
        employee_combo['values'] = list(employee_dict.keys())
        if employee_combo['values']:
            employee_combo.set(employee_combo['values'][0])

        # Leave type
        frame2 = tk.Frame(form_frame, bg="white")
        frame2.pack(fill='x', padx=20, pady=10)

        tk.Label(
            frame2,
            text="Leave Type:",
            font=("Arial", 11),
            bg="white",
            width=15,
            anchor='w'
        ).pack(side='left')

        leave_types = ['annual', 'sick', 'emergency', 'unpaid']
        leave_type_combo = ttk.Combobox(frame2, font=("Arial", 11), width=30, values=leave_types)
        leave_type_combo.pack(side='left', padx=10)
        leave_type_combo.set('annual')

        # Start date
        frame3 = tk.Frame(form_frame, bg="white")
        frame3.pack(fill='x', padx=20, pady=10)

        tk.Label(
            frame3,
            text="Start Date (YYYY-MM-DD):",
            font=("Arial", 11),
            bg="white",
            width=15,
            anchor='w'
        ).pack(side='left')

        start_entry = tk.Entry(frame3, font=("Arial", 11), width=30)
        start_entry.pack(side='left', padx=10)

        # End date
        frame4 = tk.Frame(form_frame, bg="white")
        frame4.pack(fill='x', padx=20, pady=10)

        tk.Label(
            frame4,
            text="End Date (YYYY-MM-DD):",
            font=("Arial", 11),
            bg="white",
            width=15,
            anchor='w'
        ).pack(side='left')

        end_entry = tk.Entry(frame4, font=("Arial", 11), width=30)
        end_entry.pack(side='left', padx=10)

        # Reason
        frame5 = tk.Frame(form_frame, bg="white")
        frame5.pack(fill='x', padx=20, pady=10)

        tk.Label(
            frame5,
            text="Reason:",
            font=("Arial", 11),
            bg="white",
            width=15,
            anchor='w'
        ).pack(side='left')

        reason_text = tk.Text(frame5, font=("Arial", 11), height=5, width=30)
        reason_text.pack(side='left', padx=10)

        def save():
            selected_emp = employee_combo.get()
            if not selected_emp:
                messagebox.showerror("Error", "Please select an employee")
                return

            employee_id = employee_dict.get(selected_emp)
            leave_type = leave_type_combo.get()
            start_date = start_entry.get().strip()
            end_date = end_entry.get().strip()
            reason = reason_text.get('1.0', 'end').strip()

            if not start_date or not end_date:
                messagebox.showerror("Error", "Please enter start and end dates")
                return

            result, message = self.leave_model.request(employee_id, leave_type, start_date, end_date, reason)

            if result:
                messagebox.showinfo("Success", message)
                window.destroy()
                self.load_data()
            else:
                messagebox.showerror("Error", message)

        buttons_frame = tk.Frame(form_frame, bg="white")
        buttons_frame.pack(pady=20)

        tk.Button(
            buttons_frame,
            text="💾 Submit Request",
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

    def approve_leave(self):
        """Approve leave request"""
        leave_id = self.get_selected()
        if leave_id:
            result, message = self.leave_model.approve(leave_id)
            if result:
                messagebox.showinfo("Success", message)
                self.load_data()
            else:
                messagebox.showerror("Error", message)

    def reject_leave(self):
        """Reject leave request"""
        leave_id = self.get_selected()
        if leave_id:
            result, message = self.leave_model.reject(leave_id)
            if result:
                messagebox.showinfo("Success", message)
                self.load_data()
            else:
                messagebox.showerror("Error", message)