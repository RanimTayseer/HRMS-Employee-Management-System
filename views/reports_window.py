"""
reports_window.py - Advanced Reports Window
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.report import Report


class ReportsWindow:
    """Reports Window"""
    
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame
        self.report_model = Report()
        self.setup_ui()
    
    def setup_ui(self):
        # Clear previous content
        for widget in self.parent_frame.winfo_children():
            widget.destroy()
        
        # Title
        title = tk.Label(
            self.parent_frame,
            text="📊 Advanced Reports",
            font=("Arial", 24, "bold"),
            bg="white",
            fg="#1e5799"
        )
        title.pack(pady=20)
        
        # Reports frame
        reports_frame = tk.Frame(self.parent_frame, bg="white")
        reports_frame.pack(fill='both', expand=True, padx=40, pady=20)
        
        # Employees Report
        self.create_report_card(
            reports_frame,
            "👥 Employees Report",
            "Comprehensive report of all employees with complete data",
            "📄 PDF",
            self.export_employees_report,
            0, 0
        )
        
        # Attendance Report
        self.create_report_card(
            reports_frame,
            "⏰ Attendance Report",
            "Employee check-in/check-out report for a specific month",
            "📄 PDF",
            self.export_attendance_report,
            0, 1
        )
        
        # Salary Report
        self.create_report_card(
            reports_frame,
            "💰 Salary Report",
            "Monthly salary report with allowances and deductions",
            "📄 PDF",
            self.export_salary_report,
            1, 0
        )
        
        # Statistical Chart
        self.create_report_card(
            reports_frame,
            "📈 Statistical Chart",
            "Illustrative charts showing employee distribution by department",
            "📊 Image",
            self.export_charts,
            1, 1
        )
    
    def create_report_card(self, parent, title, description, btn_text, command, row, col):
        """Create a report card"""
        card = tk.Frame(parent, bg="white", relief=tk.RAISED, bd=1, highlightthickness=1, highlightbackground="#d1d5db")
        card.grid(row=row, column=col, padx=15, pady=15, sticky='nsew')
        parent.grid_rowconfigure(row, weight=1)
        parent.grid_columnconfigure(col, weight=1)
        
        # Report title
        tk.Label(
            card,
            text=title,
            font=("Arial", 16, "bold"),
            bg="white",
            fg="#1e5799"
        ).pack(pady=(20, 10))
        
        # Separator line
        tk.Frame(card, bg="#d1d5db", height=2).pack(fill='x', padx=20, pady=5)
        
        # Description
        tk.Label(
            card,
            text=description,
            font=("Arial", 10),
            bg="white",
            fg="gray",
            wraplength=250
        ).pack(pady=10, padx=20)
        
        # Export button
        tk.Button(
            card,
            text=btn_text,
            font=("Arial", 11, "bold"),
            bg="#3498db",
            fg="white",
            padx=20,
            pady=8,
            cursor="hand2",
            command=command
        ).pack(pady=(10, 20))
    
    def export_employees_report(self):
        """Export employees report"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            initialfile=f"Employees_Report_{datetime.now().strftime('%Y%m%d')}.pdf"
        )
        
        if filename:
            try:
                self.report_model.generate_employees_report(filename)
                messagebox.showinfo("Success", f"Report created successfully\n{filename}")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")
    
    def export_attendance_report(self):
        """Export attendance report"""
        # Month selection window
        window = tk.Toplevel(self.parent_frame)
        window.title("Select Month")
        window.geometry("300x200")
        window.resizable(False, False)
        
        tk.Label(
            window,
            text="Select month for report:",
            font=("Arial", 12)
        ).pack(pady=20)
        
        now = datetime.now()
        months = []
        for y in range(now.year - 1, now.year + 1):
            for m in range(1, 13):
                months.append(f"{y}-{str(m).zfill(2)}")
        
        month_var = tk.StringVar(value=now.strftime('%Y-%m'))
        month_combo = ttk.Combobox(window, textvariable=month_var, values=months, width=15)
        month_combo.pack(pady=10)
        
        def confirm():
            filename = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf")],
                initialfile=f"Attendance_Report_{month_var.get()}.pdf"
            )
            
            if filename:
                try:
                    self.report_model.generate_attendance_report(filename, month_var.get())
                    messagebox.showinfo("Success", f"Report created successfully\n{filename}")
                    window.destroy()
                except Exception as e:
                    messagebox.showerror("Error", f"An error occurred: {e}")
        
        tk.Button(
            window,
            text="Confirm",
            bg="#2ecc71",
            fg="white",
            padx=20,
            pady=5,
            command=confirm
        ).pack(pady=20)
        
        window.grab_set()
        window.wait_window()
    
    def export_salary_report(self):
        """Export salary report"""
        # Month selection window
        window = tk.Toplevel(self.parent_frame)
        window.title("Select Month")
        window.geometry("300x200")
        window.resizable(False, False)
        
        tk.Label(
            window,
            text="Select month for report:",
            font=("Arial", 12)
        ).pack(pady=20)
        
        now = datetime.now()
        months = []
        for y in range(now.year - 1, now.year + 1):
            for m in range(1, 13):
                months.append(f"{y}-{str(m).zfill(2)}")
        
        month_var = tk.StringVar(value=now.strftime('%Y-%m'))
        month_combo = ttk.Combobox(window, textvariable=month_var, values=months, width=15)
        month_combo.pack(pady=10)
        
        def confirm():
            filename = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf")],
                initialfile=f"Salary_Report_{month_var.get()}.pdf"
            )
            
            if filename:
                try:
                    self.report_model.generate_salary_report(filename, month_var.get())
                    messagebox.showinfo("Success", f"Report created successfully\n{filename}")
                    window.destroy()
                except Exception as e:
                    messagebox.showerror("Error", f"An error occurred: {e}")
        
        tk.Button(
            window,
            text="Confirm",
            bg="#2ecc71",
            fg="white",
            padx=20,
            pady=5,
            command=confirm
        ).pack(pady=20)
        
        window.grab_set()
        window.wait_window()
    
    def export_charts(self):
        """Export statistical chart"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png")],
            initialfile=f"Statistical_Chart_{datetime.now().strftime('%Y%m%d')}.png"
        )
        
        if filename:
            try:
                self.report_model.generate_charts(filename)
                messagebox.showinfo("Success", f"Chart created successfully\n{filename}")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")