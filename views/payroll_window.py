"""
payroll_window.py - Payroll Management Window
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.payroll import Payroll
from models.employee import Employee


class PayrollWindow:
    """Payroll Management Window"""
    
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame
        self.payroll_model = Payroll()
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
            text="💰 Payroll Management",
            font=("Arial", 24, "bold"),
            bg="white",
            fg="#1e5799"
        )
        title.pack(pady=20)
        
        # Top control frame
        control_frame = tk.Frame(self.parent_frame, bg="white")
        control_frame.pack(fill='x', padx=20, pady=10)
        
        # Month selection
        tk.Label(
            control_frame,
            text="Month:",
            font=("Arial", 11),
            bg="white"
        ).pack(side='left', padx=5)
        
        # Default month and year
        now = datetime.now()
        current_month = f"{now.year}-{str(now.month).zfill(2)}"
        
        self.month_var = tk.StringVar(value=current_month)
        
        # Available months list
        months = []
        for y in range(now.year - 1, now.year + 1):
            for m in range(1, 13):
                months.append(f"{y}-{str(m).zfill(2)}")
        
        self.month_combo = ttk.Combobox(
            control_frame,
            textvariable=self.month_var,
            values=months,
            font=("Arial", 11),
            width=15
        )
        self.month_combo.pack(side='left', padx=5)
        
        # Process payroll button
        process_btn = tk.Button(
            control_frame,
            text="🧮 Process Payroll",
            font=("Arial", 11, "bold"),
            bg="#2ecc71",
            fg="white",
            padx=15,
            pady=8,
            cursor="hand2",
            command=self.process_payroll
        )
        process_btn.pack(side='left', padx=5)
        
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
        
        # Export button
        export_btn = tk.Button(
            control_frame,
            text="📎 Export to Excel",
            font=("Arial", 11),
            bg="#95a5a6",
            fg="white",
            padx=15,
            pady=8,
            cursor="hand2",
            command=self.export_to_excel
        )
        export_btn.pack(side='left', padx=5)
        
        # Table frame
        table_frame = tk.Frame(self.parent_frame, bg="white")
        table_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Create table
        columns = ('ID', 'Employee ID', 'Employee', 'Department', 'Basic Salary', 'Allowances', 'Deductions', 'Net Salary', 'Status')
        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=20)
        
        widths = [50, 100, 150, 120, 120, 100, 100, 130, 80]
        for col, width in zip(columns, widths):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Statistics frame
        stats_frame = tk.Frame(self.parent_frame, bg="white")
        stats_frame.pack(fill='x', padx=20, pady=10)
        
        self.stats_label = tk.Label(
            stats_frame,
            text="",
            font=("Arial", 11),
            bg="white",
            fg="#1e5799"
        )
        self.stats_label.pack()
        
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
        """Load payroll data into table"""
        # Clear old data
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        month = self.month_var.get()
        payrolls = self.payroll_model.get_by_month(month)
        
        if not payrolls:
            self.status_label.config(text="⚠️ No payroll records found for this month. Click 'Process Payroll'")
            self.stats_label.config(text="")
            return
        
        total_salaries = 0
        for p in payrolls:
            net_salary = p.get('net_salary', 0) or 0
            total_salaries += net_salary
            
            self.tree.insert('', 'end', values=(
                p.get('payroll_id', ''),
                p.get('employee_number', ''),
                p.get('full_name', ''),
                p.get('department_name', ''),
                f"{p.get('basic_salary', 0):,.2f}",
                f"{p.get('allowances', 0):,.2f}",
                f"{p.get('deductions', 0):,.2f}",
                f"{net_salary:,.2f}",
                'Paid' if p.get('paid_at') else 'Unpaid'
            ))
        
        self.status_label.config(text=f"📊 Total Employees: {len(payrolls)}")
        self.stats_label.config(text=f"💰 Total Salaries for this month: {total_salaries:,.2f}")
    
    def process_payroll(self):
        """Process and calculate payroll"""
        month = self.month_var.get()
        
        if not month:
            messagebox.showerror("Error", "Please select a month")
            return
        
        # Confirmation
        if not messagebox.askyesno("Confirm", f"Do you want to process payroll for {month}?"):
            return
        
        self.status_label.config(text="🔄 Processing payroll...")
        self.parent_frame.update()
        
        # Process payroll
        result = self.payroll_model.process_payroll(month)
        
        if result and result > 0:
            messagebox.showinfo("Success", f"Payroll processed for {result} employee(s) successfully")
            self.load_data()
        else:
            messagebox.showwarning("Warning", "No employees found to process payroll")
        
        self.status_label.config(text="")
    
    def export_to_excel(self):
        """Export data to Excel"""
        month = self.month_var.get()
        payrolls = self.payroll_model.get_by_month(month)
        
        if not payrolls:
            messagebox.showwarning("Warning", "No data to export")
            return
        
        try:
            import pandas as pd
            
            # Convert data to DataFrame
            data = []
            for p in payrolls:
                data.append({
                    'Employee ID': p.get('employee_number', ''),
                    'Employee Name': p.get('full_name', ''),
                    'Department': p.get('department_name', ''),
                    'Basic Salary': p.get('basic_salary', 0),
                    'Allowances': p.get('allowances', 0),
                    'Overtime': p.get('overtime_amount', 0),
                    'Deductions': p.get('deductions', 0),
                    'Net Salary': p.get('net_salary', 0),
                    'Status': 'Paid' if p.get('paid_at') else 'Unpaid'
                })
            
            df = pd.DataFrame(data)
            
            # Save file
            from tkinter import filedialog
            filename = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx")],
                initialfile=f"Payroll_{month}.xlsx"
            )
            
            if filename:
                df.to_excel(filename, index=False)
                messagebox.showinfo("Success", f"Data exported successfully to {filename}")
        
        except ImportError:
            messagebox.showerror("Error", "Pandas library not installed. Install it using: pip install pandas openpyxl")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")