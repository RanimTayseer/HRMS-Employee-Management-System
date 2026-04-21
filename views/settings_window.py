"""
settings_window.py - Settings Window
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os
import shutil
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db_manager import db
from utils.session_manager import session


class SettingsWindow:
    """Settings Window"""
    
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame
        self.setup_ui()
        self.load_settings()
    
    def setup_ui(self):
        # Clear previous content
        for widget in self.parent_frame.winfo_children():
            widget.destroy()
        
        # Title
        title = tk.Label(
            self.parent_frame,
            text="⚙️ Settings",
            font=("Arial", 24, "bold"),
            bg="white",
            fg="#1e5799"
        )
        title.pack(pady=20)
        
        # Create notebook (tabs)
        self.notebook = ttk.Notebook(self.parent_frame)
        self.notebook.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Tab 1: General Settings
        self.general_tab = tk.Frame(self.notebook, bg="white")
        self.notebook.add(self.general_tab, text="📋 General")
        self.setup_general_tab()
        
        # Tab 2: Email Settings
        self.email_tab = tk.Frame(self.notebook, bg="white")
        self.notebook.add(self.email_tab, text="📧 Email")
        self.setup_email_tab()
        
        # Tab 3: Company Settings
        self.company_tab = tk.Frame(self.notebook, bg="white")
        self.notebook.add(self.company_tab, text="🏢 Company")
        self.setup_company_tab()
        
        # Tab 4: Payroll Settings
        self.payroll_tab = tk.Frame(self.notebook, bg="white")
        self.notebook.add(self.payroll_tab, text="💰 Payroll")
        self.setup_payroll_tab()
        
        # Tab 5: Backup & Restore
        self.backup_tab = tk.Frame(self.notebook, bg="white")
        self.notebook.add(self.backup_tab, text="💾 Backup")
        self.setup_backup_tab()
        
        # Tab 6: Users
        self.users_tab = tk.Frame(self.notebook, bg="white")
        self.notebook.add(self.users_tab, text="👥 Users")
        self.setup_users_tab()
    
    def load_settings(self):
        """Load settings from database or config file"""
        from utils.config_manager import config
        # Load saved settings
        theme = config.get('theme', 'light')
        language = config.get('language', 'english')
        
        # Update UI
        if theme == 'light':
            self.theme_var.set('Light')
        elif theme == 'dark':
            self.theme_var.set('Dark')
        elif theme == 'blue':
            self.theme_var.set('Blue')
        
        if language == 'english':
            self.language_var.set('English')
        else:
            self.language_var.set('Arabic')
        
        # Load email settings
        self.email_enabled_var.set(config.get('email_enabled', False))
        self.sender_email_entry.delete(0, tk.END)
        self.sender_email_entry.insert(0, config.get('sender_email', ''))
        self.sender_password_entry.delete(0, tk.END)
        self.sender_password_entry.insert(0, config.get('sender_password', ''))
        self.admin_email_entry.delete(0, tk.END)
        self.admin_email_entry.insert(0, config.get('admin_email', 'admin@company.com'))
        self.finance_email_entry.delete(0, tk.END)
        self.finance_email_entry.insert(0, config.get('finance_email', 'finance@company.com'))
    
    # ==================== General Tab ====================
    def setup_general_tab(self):
        """Setup general settings tab"""
        frame = tk.Frame(self.general_tab, bg="white")
        frame.pack(fill='both', expand=True, padx=30, pady=20)
        
        # App Language
        row1 = tk.Frame(frame, bg="white")
        row1.pack(fill='x', pady=10)
        tk.Label(row1, text="Application Language:", font=("Arial", 11), bg="white", width=25, anchor='w').pack(side='left')
        self.language_var = tk.StringVar(value="English")
        lang_combo = ttk.Combobox(row1, textvariable=self.language_var, values=["English", "Arabic"], width=20)
        lang_combo.pack(side='left', padx=10)
        
        # Date Format
        row2 = tk.Frame(frame, bg="white")
        row2.pack(fill='x', pady=10)
        tk.Label(row2, text="Date Format:", font=("Arial", 11), bg="white", width=25, anchor='w').pack(side='left')
        self.date_format_var = tk.StringVar(value="YYYY-MM-DD")
        date_combo = ttk.Combobox(row2, textvariable=self.date_format_var, values=["YYYY-MM-DD", "DD-MM-YYYY", "MM-DD-YYYY"], width=20)
        date_combo.pack(side='left', padx=10)
        
        # Theme
        row3 = tk.Frame(frame, bg="white")
        row3.pack(fill='x', pady=10)
        tk.Label(row3, text="Theme:", font=("Arial", 11), bg="white", width=25, anchor='w').pack(side='left')
        self.theme_var = tk.StringVar(value="Light")
        theme_combo = ttk.Combobox(row3, textvariable=self.theme_var, values=["Light", "Dark", "Blue"], width=20)
        theme_combo.pack(side='left', padx=10)
        
        # Items per page
        row4 = tk.Frame(frame, bg="white")
        row4.pack(fill='x', pady=10)
        tk.Label(row4, text="Items Per Page:", font=("Arial", 11), bg="white", width=25, anchor='w').pack(side='left')
        self.items_per_page_var = tk.StringVar(value="50")
        items_combo = ttk.Combobox(row4, textvariable=self.items_per_page_var, values=["20", "50", "100", "200"], width=20)
        items_combo.pack(side='left', padx=10)
        
        # Separator
        tk.Frame(frame, bg="#d1d5db", height=2).pack(fill='x', pady=20)
        
        # Save button
        btn_frame = tk.Frame(frame, bg="white")
        btn_frame.pack(pady=20)
        tk.Button(
            btn_frame,
            text="💾 Save General Settings",
            font=("Arial", 11, "bold"),
            bg="#2ecc71",
            fg="white",
            padx=20,
            pady=8,
            cursor="hand2",
            command=self.save_general_settings
        ).pack()
    
    def save_general_settings(self):
        """Save general settings and apply changes"""
        from utils.config_manager import config
        
        # Get values
        language = self.language_var.get().lower()
        theme = self.theme_var.get().lower()
        items_per_page = self.items_per_page_var.get()
        
        # Save to config
        config.set('language', 'english' if language == 'english' else 'arabic')
        config.set('theme', theme)
        config.set('items_per_page', int(items_per_page))
        
        messagebox.showinfo("Success", "Settings saved! Please restart the application for language changes to take effect.")
        
        # Apply theme immediately
        self.apply_theme_to_parent(theme)
    
    # ==================== Email Tab ====================
    def setup_email_tab(self):
        """Setup email settings tab"""
        frame = tk.Frame(self.email_tab, bg="white")
        frame.pack(fill='both', expand=True, padx=30, pady=20)
        
        # Enable Email Notifications
        row1 = tk.Frame(frame, bg="white")
        row1.pack(fill='x', pady=10)
        self.email_enabled_var = tk.BooleanVar(value=False)
        tk.Checkbutton(
            row1, 
            text="Enable Email Notifications", 
            variable=self.email_enabled_var, 
            bg="white", 
            font=("Arial", 11, "bold")
        ).pack(anchor='w', padx=10)
        
        # Separator
        tk.Frame(frame, bg="#d1d5db", height=2).pack(fill='x', pady=10)
        
        # Sender Email
        row2 = tk.Frame(frame, bg="white")
        row2.pack(fill='x', pady=10)
        tk.Label(row2, text="Sender Email (Gmail):", font=("Arial", 11), bg="white", width=20, anchor='w').pack(side='left')
        self.sender_email_entry = tk.Entry(row2, font=("Arial", 11), width=35)
        self.sender_email_entry.pack(side='left', padx=10)
        
        # Email Password
        row3 = tk.Frame(frame, bg="white")
        row3.pack(fill='x', pady=10)
        tk.Label(row3, text="Email Password/App Password:", font=("Arial", 11), bg="white", width=20, anchor='w').pack(side='left')
        self.sender_password_entry = tk.Entry(row3, font=("Arial", 11), show="*", width=35)
        self.sender_password_entry.pack(side='left', padx=10)
        
        # Admin Email
        row4 = tk.Frame(frame, bg="white")
        row4.pack(fill='x', pady=10)
        tk.Label(row4, text="Admin Email (for notifications):", font=("Arial", 11), bg="white", width=20, anchor='w').pack(side='left')
        self.admin_email_entry = tk.Entry(row4, font=("Arial", 11), width=35)
        self.admin_email_entry.pack(side='left', padx=10)
        self.admin_email_entry.insert(0, "admin@company.com")
        
        # Finance Email
        row5 = tk.Frame(frame, bg="white")
        row5.pack(fill='x', pady=10)
        tk.Label(row5, text="Finance Email (for payroll):", font=("Arial", 11), bg="white", width=20, anchor='w').pack(side='left')
        self.finance_email_entry = tk.Entry(row5, font=("Arial", 11), width=35)
        self.finance_email_entry.pack(side='left', padx=10)
        self.finance_email_entry.insert(0, "finance@company.com")
        
        # Info
        info_frame = tk.LabelFrame(frame, text="ℹ️ How to Setup Email", font=("Arial", 10, "bold"), bg="white", fg="#1e5799")
        info_frame.pack(fill='x', pady=20)
        
        info_text = """
For Gmail:
1. Go to your Google Account settings
2. Enable 2-Factor Authentication
3. Generate an App Password
4. Use that password here

OR use a regular password with "Less secure app access" enabled.
        """
        tk.Label(
            info_frame,
            text=info_text,
            font=("Arial", 9),
            bg="white",
            fg="gray",
            justify="left"
        ).pack(pady=10, padx=10)
        
        # Separator
        tk.Frame(frame, bg="#d1d5db", height=2).pack(fill='x', pady=10)
        
        # Save button
        btn_frame = tk.Frame(frame, bg="white")
        btn_frame.pack(pady=20)
        tk.Button(
            btn_frame,
            text="💾 Save Email Settings",
            font=("Arial", 11, "bold"),
            bg="#2ecc71",
            fg="white",
            padx=20,
            pady=8,
            cursor="hand2",
            command=self.save_email_settings
        ).pack()
        
        # Test button
        tk.Button(
            btn_frame,
            text="📧 Test Email",
            font=("Arial", 11),
            bg="#3498db",
            fg="white",
            padx=20,
            pady=8,
            cursor="hand2",
            command=self.test_email
        ).pack(side='left', padx=10)
    
    def save_email_settings(self):
        """Save email settings"""
        from utils.config_manager import config
        from utils.email_notifier import email_notifier
        
        email_enabled = self.email_enabled_var.get()
        sender_email = self.sender_email_entry.get().strip()
        sender_password = self.sender_password_entry.get().strip()
        admin_email = self.admin_email_entry.get().strip()
        finance_email = self.finance_email_entry.get().strip()
        
        # Save to config
        config.set('email_enabled', email_enabled)
        config.set('sender_email', sender_email)
        config.set('sender_password', sender_password)
        config.set('admin_email', admin_email)
        config.set('finance_email', finance_email)
        
        # Configure email notifier
        if email_enabled and sender_email and sender_password:
            email_notifier.configure(sender_email, sender_password, True)
            messagebox.showinfo("Success", "Email settings saved and enabled successfully!")
        else:
            email_notifier.configure("", "", False)
            messagebox.showinfo("Success", "Email settings saved (notifications disabled)")
    
    def test_email(self):
        """Send test email"""
        from utils.config_manager import config
        from utils.email_notifier import email_notifier
        
        admin_email = self.admin_email_entry.get().strip()
        
        if not admin_email:
            messagebox.showerror("Error", "Please enter admin email address")
            return
        
        email_notifier.configure(
            self.sender_email_entry.get().strip(),
            self.sender_password_entry.get().strip(),
            True
        )
        
        subject = "HRMS Test Email"
        body = """
        <html>
        <body>
            <h2>Test Email from HRMS System</h2>
            <p>This is a test email to verify that email notifications are working correctly.</p>
            <p>If you received this email, your email settings are configured properly!</p>
            <br>
            <p>Best regards,</p>
            <p><strong>HRMS System</strong></p>
        </body>
        </html>
        """
        
        if email_notifier.send_email(admin_email, subject, body):
            messagebox.showinfo("Success", f"Test email sent to {admin_email}")
        else:
            messagebox.showerror("Error", "Failed to send test email. Please check your settings.")
    
    def apply_theme_to_parent(self, theme):
        """Apply theme to parent window"""
        from utils.config_manager import config
        
        # Temporarily set theme to get colors
        old_theme = config.get('theme')
        config.set('theme', theme)
        colors = config.get_theme_colors()
        
        # Apply to parent frame
        self.parent_frame.configure(bg=colors['white'])
        
        # Update all children
        self.apply_theme_to_widget(self.parent_frame, colors)
        
        # Also update notebook background
        self.notebook.configure(bg=colors['white'])
        
        # Restore old theme setting
        config.set('theme', old_theme)
    
    def apply_theme_to_widget(self, widget, colors):
        """Recursively apply theme to widget and children"""
        try:
            if isinstance(widget, tk.Frame):
                widget.configure(bg=colors['white'])
            elif isinstance(widget, tk.Label):
                current_bg = widget.cget('bg')
                if current_bg not in ['#f0f4f8', 'white', '#ffffff']:
                    pass
                else:
                    widget.configure(bg=colors['white'], fg=colors['fg'])
            elif isinstance(widget, tk.Button):
                pass
            elif isinstance(widget, tk.Entry):
                widget.configure(bg=colors['entry_bg'], fg=colors['fg'], insertbackground=colors['fg'])
            elif isinstance(widget, ttk.Combobox):
                pass
            elif isinstance(widget, ttk.Notebook):
                widget.configure(bg=colors['white'])
            
            for child in widget.winfo_children():
                self.apply_theme_to_widget(child, colors)
        except:
            pass
    
    # ==================== Company Tab ====================
    def setup_company_tab(self):
        """Setup company settings tab"""
        frame = tk.Frame(self.company_tab, bg="white")
        frame.pack(fill='both', expand=True, padx=30, pady=20)
        
        # Company Name
        row1 = tk.Frame(frame, bg="white")
        row1.pack(fill='x', pady=10)
        tk.Label(row1, text="Company Name:", font=("Arial", 11), bg="white", width=25, anchor='w').pack(side='left')
        self.company_name_entry = tk.Entry(row1, font=("Arial", 11), width=30)
        self.company_name_entry.pack(side='left', padx=10)
        self.company_name_entry.insert(0, "My Company")
        
        # Company Address
        row2 = tk.Frame(frame, bg="white")
        row2.pack(fill='x', pady=10)
        tk.Label(row2, text="Company Address:", font=("Arial", 11), bg="white", width=25, anchor='w').pack(side='left')
        self.company_address_entry = tk.Entry(row2, font=("Arial", 11), width=30)
        self.company_address_entry.pack(side='left', padx=10)
        
        # Company Phone
        row3 = tk.Frame(frame, bg="white")
        row3.pack(fill='x', pady=10)
        tk.Label(row3, text="Company Phone:", font=("Arial", 11), bg="white", width=25, anchor='w').pack(side='left')
        self.company_phone_entry = tk.Entry(row3, font=("Arial", 11), width=30)
        self.company_phone_entry.pack(side='left', padx=10)
        
        # Company Email
        row4 = tk.Frame(frame, bg="white")
        row4.pack(fill='x', pady=10)
        tk.Label(row4, text="Company Email:", font=("Arial", 11), bg="white", width=25, anchor='w').pack(side='left')
        self.company_email_entry = tk.Entry(row4, font=("Arial", 11), width=30)
        self.company_email_entry.pack(side='left', padx=10)
        
        # Tax Number
        row5 = tk.Frame(frame, bg="white")
        row5.pack(fill='x', pady=10)
        tk.Label(row5, text="Tax Number / VAT:", font=("Arial", 11), bg="white", width=25, anchor='w').pack(side='left')
        self.tax_number_entry = tk.Entry(row5, font=("Arial", 11), width=30)
        self.tax_number_entry.pack(side='left', padx=10)
        
        # Separator
        tk.Frame(frame, bg="#d1d5db", height=2).pack(fill='x', pady=20)
        
        # Save button
        btn_frame = tk.Frame(frame, bg="white")
        btn_frame.pack(pady=20)
        tk.Button(
            btn_frame,
            text="💾 Save Company Settings",
            font=("Arial", 11, "bold"),
            bg="#2ecc71",
            fg="white",
            padx=20,
            pady=8,
            cursor="hand2",
            command=self.save_company_settings
        ).pack()
    
    def save_company_settings(self):
        """Save company settings"""
        from utils.config_manager import config
        config.set('company_name', self.company_name_entry.get())
        config.set('company_address', self.company_address_entry.get())
        config.set('company_phone', self.company_phone_entry.get())
        config.set('company_email', self.company_email_entry.get())
        config.set('tax_number', self.tax_number_entry.get())
        messagebox.showinfo("Success", "Company settings saved successfully!")
    
    # ==================== Payroll Tab ====================
    def setup_payroll_tab(self):
        """Setup payroll settings tab"""
        frame = tk.Frame(self.payroll_tab, bg="white")
        frame.pack(fill='both', expand=True, padx=30, pady=20)
        
        # Working Hours per Day
        row1 = tk.Frame(frame, bg="white")
        row1.pack(fill='x', pady=10)
        tk.Label(row1, text="Working Hours per Day:", font=("Arial", 11), bg="white", width=25, anchor='w').pack(side='left')
        self.working_hours_var = tk.StringVar(value="8")
        hours_entry = tk.Entry(row1, font=("Arial", 11), textvariable=self.working_hours_var, width=20)
        hours_entry.pack(side='left', padx=10)
        
        # Overtime Rate
        row2 = tk.Frame(frame, bg="white")
        row2.pack(fill='x', pady=10)
        tk.Label(row2, text="Overtime Rate (x):", font=("Arial", 11), bg="white", width=25, anchor='w').pack(side='left')
        self.overtime_rate_var = tk.StringVar(value="1.5")
        overtime_entry = tk.Entry(row2, font=("Arial", 11), textvariable=self.overtime_rate_var, width=20)
        overtime_entry.pack(side='left', padx=10)
        
        # Late Deduction per Minute
        row3 = tk.Frame(frame, bg="white")
        row3.pack(fill='x', pady=10)
        tk.Label(row3, text="Late Deduction (per minute):", font=("Arial", 11), bg="white", width=25, anchor='w').pack(side='left')
        self.late_deduction_var = tk.StringVar(value="0.5")
        late_entry = tk.Entry(row3, font=("Arial", 11), textvariable=self.late_deduction_var, width=20)
        late_entry.pack(side='left', padx=10)
        
        # Social Security Rate
        row4 = tk.Frame(frame, bg="white")
        row4.pack(fill='x', pady=10)
        tk.Label(row4, text="Social Security Rate (%):", font=("Arial", 11), bg="white", width=25, anchor='w').pack(side='left')
        self.ss_rate_var = tk.StringVar(value="7.5")
        ss_entry = tk.Entry(row4, font=("Arial", 11), textvariable=self.ss_rate_var, width=20)
        ss_entry.pack(side='left', padx=10)
        
        # Tax Rate
        row5 = tk.Frame(frame, bg="white")
        row5.pack(fill='x', pady=10)
        tk.Label(row5, text="Tax Rate (%):", font=("Arial", 11), bg="white", width=25, anchor='w').pack(side='left')
        self.tax_rate_var = tk.StringVar(value="10")
        tax_entry = tk.Entry(row5, font=("Arial", 11), textvariable=self.tax_rate_var, width=20)
        tax_entry.pack(side='left', padx=10)
        
        # Currency
        row6 = tk.Frame(frame, bg="white")
        row6.pack(fill='x', pady=10)
        tk.Label(row6, text="Currency:", font=("Arial", 11), bg="white", width=25, anchor='w').pack(side='left')
        self.currency_var = tk.StringVar(value="SAR")
        currency_combo = ttk.Combobox(row6, textvariable=self.currency_var, values=["SAR", "USD", "EUR", "AED"], width=18)
        currency_combo.pack(side='left', padx=10)
        
        # Separator
        tk.Frame(frame, bg="#d1d5db", height=2).pack(fill='x', pady=20)
        
        # Save button
        btn_frame = tk.Frame(frame, bg="white")
        btn_frame.pack(pady=20)
        tk.Button(
            btn_frame,
            text="💾 Save Payroll Settings",
            font=("Arial", 11, "bold"),
            bg="#2ecc71",
            fg="white",
            padx=20,
            pady=8,
            cursor="hand2",
            command=self.save_payroll_settings
        ).pack()
    
    def save_payroll_settings(self):
        """Save payroll settings"""
        from utils.config_manager import config
        config.set('working_hours', int(self.working_hours_var.get()))
        config.set('overtime_rate', float(self.overtime_rate_var.get()))
        config.set('late_deduction', float(self.late_deduction_var.get()))
        config.set('ss_rate', float(self.ss_rate_var.get()))
        config.set('tax_rate', float(self.tax_rate_var.get()))
        config.set('currency', self.currency_var.get())
        messagebox.showinfo("Success", "Payroll settings saved successfully!")
    
    # ==================== Backup Tab ====================
    def setup_backup_tab(self):
        """Setup backup and restore tab"""
        frame = tk.Frame(self.backup_tab, bg="white")
        frame.pack(fill='both', expand=True, padx=30, pady=20)
        
        # Backup section
        backup_frame = tk.LabelFrame(frame, text="💾 Backup Database", font=("Arial", 12, "bold"), bg="white", fg="#1e5799")
        backup_frame.pack(fill='x', pady=10)
        
        tk.Label(
            backup_frame,
            text="Create a backup of your entire database.",
            font=("Arial", 10),
            bg="white",
            fg="gray"
        ).pack(pady=10)
        
        tk.Button(
            backup_frame,
            text="📀 Create Backup",
            font=("Arial", 11, "bold"),
            bg="#3498db",
            fg="white",
            padx=20,
            pady=8,
            cursor="hand2",
            command=self.create_backup
        ).pack(pady=10)
        
        # Restore section
        restore_frame = tk.LabelFrame(frame, text="🔄 Restore Database", font=("Arial", 12, "bold"), bg="white", fg="#1e5799")
        restore_frame.pack(fill='x', pady=10)
        
        tk.Label(
            restore_frame,
            text="Restore database from a backup file.",
            font=("Arial", 10),
            bg="white",
            fg="gray"
        ).pack(pady=10)
        
        tk.Button(
            restore_frame,
            text="📂 Restore from Backup",
            font=("Arial", 11, "bold"),
            bg="#e74c3c",
            fg="white",
            padx=20,
            pady=8,
            cursor="hand2",
            command=self.restore_backup
        ).pack(pady=10)
        
        # Auto Backup section
        auto_frame = tk.LabelFrame(frame, text="🤖 Auto Backup", font=("Arial", 12, "bold"), bg="white", fg="#1e5799")
        auto_frame.pack(fill='x', pady=10)
        
        self.auto_backup_var = tk.BooleanVar(value=False)
        tk.Checkbutton(
            auto_frame,
            text="Enable Automatic Backup",
            variable=self.auto_backup_var,
            font=("Arial", 11),
            bg="white"
        ).pack(pady=10)
        
        tk.Button(
            auto_frame,
            text="💾 Save Auto Backup Settings",
            font=("Arial", 11),
            bg="#2ecc71",
            fg="white",
            padx=20,
            pady=8,
            cursor="hand2",
            command=self.save_auto_backup
        ).pack(pady=10)
    
    def create_backup(self):
        """Create database backup"""
        try:
            from tkinter import filedialog
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filename = filedialog.asksaveasfilename(
                defaultextension=".db",
                filetypes=[("Database files", "*.db")],
                initialfile=f"backup_{timestamp}.db"
            )
            
            if backup_filename:
                shutil.copy2("personnel.db", backup_filename)
                messagebox.showinfo("Success", f"Backup created successfully!\n{backup_filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Backup failed: {e}")
    
    def restore_backup(self):
        """Restore database from backup"""
        try:
            from tkinter import filedialog
            backup_file = filedialog.askopenfilename(
                filetypes=[("Database files", "*.db"), ("All files", "*.*")]
            )
            
            if backup_file:
                if messagebox.askyesno("Confirm", "Restoring will overwrite current data. Are you sure?"):
                    shutil.copy2(backup_file, "personnel.db")
                    messagebox.showinfo("Success", "Database restored successfully! Please restart the application.")
        except Exception as e:
            messagebox.showerror("Error", f"Restore failed: {e}")
    
    def save_auto_backup(self):
        """Save auto backup settings"""
        from utils.config_manager import config
        config.set('auto_backup', self.auto_backup_var.get())
        messagebox.showinfo("Success", "Auto backup settings saved successfully!")
    
    # ==================== Users Tab ====================
    def setup_users_tab(self):
        """Setup users management tab"""
        frame = tk.Frame(self.users_tab, bg="white")
        frame.pack(fill='both', expand=True, padx=30, pady=20)
        
        # Only admin can manage users
        if session.user_role != 'admin':
            tk.Label(
                frame,
                text="⚠️ Only Administrators can manage users.",
                font=("Arial", 14),
                bg="white",
                fg="#e74c3c"
            ).pack(expand=True)
            return
        
        # Users list
        tk.Label(
            frame,
            text="System Users",
            font=("Arial", 16, "bold"),
            bg="white",
            fg="#1e5799"
        ).pack(pady=10)
        
        # Table frame
        table_frame = tk.Frame(frame, bg="white")
        table_frame.pack(fill='both', expand=True, pady=10)
        
        # Create table
        columns = ('ID', 'Username', 'Role', 'Status', 'Last Login')
        self.users_tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=10)
        
        for col in columns:
            self.users_tree.heading(col, text=col)
            self.users_tree.column(col, width=120)
        
        scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=self.users_tree.yview)
        self.users_tree.configure(yscrollcommand=scrollbar.set)
        
        self.users_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Load users
        self.load_users()
        
        # Buttons frame
        btn_frame = tk.Frame(frame, bg="white")
        btn_frame.pack(pady=10)
        
        # Add user button
        tk.Button(
            btn_frame,
            text="➕ Add New User",
            font=("Arial", 11, "bold"),
            bg="#2ecc71",
            fg="white",
            padx=20,
            pady=8,
            cursor="hand2",
            command=self.add_user
        ).pack(side='left', padx=5)
        
        # Edit user button
        tk.Button(
            btn_frame,
            text="✏️ Edit User",
            font=("Arial", 11, "bold"),
            bg="#3498db",
            fg="white",
            padx=20,
            pady=8,
            cursor="hand2",
            command=self.edit_user
        ).pack(side='left', padx=5)
        
        # Delete user button
        tk.Button(
            btn_frame,
            text="🗑️ Delete User",
            font=("Arial", 11, "bold"),
            bg="#e74c3c",
            fg="white",
            padx=20,
            pady=8,
            cursor="hand2",
            command=self.delete_user
        ).pack(side='left', padx=5)
        
        # Refresh button
        tk.Button(
            btn_frame,
            text="🔄 Refresh",
            font=("Arial", 11),
            bg="#95a5a6",
            fg="white",
            padx=20,
            pady=8,
            cursor="hand2",
            command=self.load_users
        ).pack(side='left', padx=5)

    def load_users(self):
        """Load users from database"""
        # Clear old data
        for item in self.users_tree.get_children():
            self.users_tree.delete(item)
        
        # Get users
        query = "SELECT user_id, username, role, is_active, last_login FROM users"
        users = db.execute_query(query)
        
        for user in users:
            self.users_tree.insert('', 'end', values=(
                user.get('user_id', ''),
                user.get('username', ''),
                user.get('role', ''),
                'Active' if user.get('is_active') else 'Inactive',
                user.get('last_login', 'Never')
            ))

    def get_selected_user(self):
        """Get selected user ID"""
        selected = self.users_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a user first")
            return None
        values = self.users_tree.item(selected[0])['values']
        return values[0]

    def add_user(self):
        """Open add user dialog"""
        dialog = tk.Toplevel(self.parent_frame)
        dialog.title("Add New User")
        dialog.geometry("400x400")
        dialog.resizable(False, False)
        dialog.configure(bg="#f0f4f8")
        
        tk.Label(
            dialog,
            text="➕ Add New User",
            font=("Arial", 16, "bold"),
            bg="#f0f4f8",
            fg="#1e5799"
        ).pack(pady=20)
        
        form_frame = tk.Frame(dialog, bg="white", relief=tk.RAISED)
        form_frame.pack(fill='both', expand=True, padx=30, pady=10)
        
        # Username
        row1 = tk.Frame(form_frame, bg="white")
        row1.pack(fill='x', pady=10)
        tk.Label(row1, text="Username:", font=("Arial", 11), bg="white", width=15, anchor='w').pack(side='left')
        username_entry = tk.Entry(row1, font=("Arial", 11), width=25)
        username_entry.pack(side='left', padx=10)
        
        # Password
        row2 = tk.Frame(form_frame, bg="white")
        row2.pack(fill='x', pady=10)
        tk.Label(row2, text="Password:", font=("Arial", 11), bg="white", width=15, anchor='w').pack(side='left')
        password_entry = tk.Entry(row2, font=("Arial", 11), show="*", width=25)
        password_entry.pack(side='left', padx=10)
        
        # Confirm Password
        row3 = tk.Frame(form_frame, bg="white")
        row3.pack(fill='x', pady=10)
        tk.Label(row3, text="Confirm Password:", font=("Arial", 11), bg="white", width=15, anchor='w').pack(side='left')
        confirm_entry = tk.Entry(row3, font=("Arial", 11), show="*", width=25)
        confirm_entry.pack(side='left', padx=10)
        
        # Role
        row4 = tk.Frame(form_frame, bg="white")
        row4.pack(fill='x', pady=10)
        tk.Label(row4, text="Role:", font=("Arial", 11), bg="white", width=15, anchor='w').pack(side='left')
        role_var = tk.StringVar(value="employee")
        role_combo = ttk.Combobox(row4, textvariable=role_var, values=["admin", "hr_manager", "employee"], width=23)
        role_combo.pack(side='left', padx=10)
        
        # Status
        row5 = tk.Frame(form_frame, bg="white")
        row5.pack(fill='x', pady=10)
        tk.Label(row5, text="Status:", font=("Arial", 11), bg="white", width=15, anchor='w').pack(side='left')
        status_var = tk.BooleanVar(value=True)
        tk.Checkbutton(row5, text="Active", variable=status_var, bg="white", font=("Arial", 11)).pack(side='left', padx=10)
        
        def save_user():
            username = username_entry.get().strip()
            password = password_entry.get().strip()
            confirm = confirm_entry.get().strip()
            
            if not username or not password:
                messagebox.showerror("Error", "Please enter username and password")
                return
            
            if password != confirm:
                messagebox.showerror("Error", "Passwords do not match")
                return
            
            # Check if user exists
            check = db.execute_query("SELECT * FROM users WHERE username = ?", (username,))
            if check:
                messagebox.showerror("Error", "Username already exists")
                return
            
            # Add user
            result = db.execute_command(
                "INSERT INTO users (username, password_hash, role, is_active) VALUES (?, ?, ?, ?)",
                (username, password, role_var.get(), 1 if status_var.get() else 0)
            )
            
            if result:
                messagebox.showinfo("Success", "User added successfully!")
                dialog.destroy()
                self.load_users()
            else:
                messagebox.showerror("Error", "Failed to add user")
        
        btn_frame = tk.Frame(form_frame, bg="white")
        btn_frame.pack(pady=20)
        
        tk.Button(
            btn_frame,
            text="💾 Save",
            font=("Arial", 11, "bold"),
            bg="#2ecc71",
            fg="white",
            padx=30,
            pady=8,
            command=save_user
        ).pack(side='left', padx=10)
        
        tk.Button(
            btn_frame,
            text="❌ Cancel",
            font=("Arial", 11),
            bg="#95a5a6",
            fg="white",
            padx=30,
            pady=8,
            command=dialog.destroy
        ).pack(side='left', padx=10)

    def edit_user(self):
        """Edit selected user"""
        user_id = self.get_selected_user()
        if not user_id:
            return
        
        # Get user data
        query = "SELECT * FROM users WHERE user_id = ?"
        users = db.execute_query(query, (user_id,))
        
        if not users:
            messagebox.showerror("Error", "User not found")
            return
        
        user = users[0]
        
        # Edit dialog
        dialog = tk.Toplevel(self.parent_frame)
        dialog.title("Edit User")
        dialog.geometry("400x450")
        dialog.resizable(False, False)
        dialog.configure(bg="#f0f4f8")
        
        tk.Label(
            dialog,
            text="✏️ Edit User",
            font=("Arial", 16, "bold"),
            bg="#f0f4f8",
            fg="#1e5799"
        ).pack(pady=20)
        
        form_frame = tk.Frame(dialog, bg="white", relief=tk.RAISED)
        form_frame.pack(fill='both', expand=True, padx=30, pady=10)
        
        # Username (read-only)
        row1 = tk.Frame(form_frame, bg="white")
        row1.pack(fill='x', pady=10)
        tk.Label(row1, text="Username:", font=("Arial", 11), bg="white", width=15, anchor='w').pack(side='left')
        username_label = tk.Label(row1, text=user.get('username', ''), font=("Arial", 11, "bold"), bg="white", fg="#1e5799")
        username_label.pack(side='left', padx=10)
        
        # New Password
        row2 = tk.Frame(form_frame, bg="white")
        row2.pack(fill='x', pady=10)
        tk.Label(row2, text="New Password:", font=("Arial", 11), bg="white", width=15, anchor='w').pack(side='left')
        password_entry = tk.Entry(row2, font=("Arial", 11), show="*", width=25)
        password_entry.pack(side='left', padx=10)
        
        # Confirm Password
        row3 = tk.Frame(form_frame, bg="white")
        row3.pack(fill='x', pady=10)
        tk.Label(row3, text="Confirm Password:", font=("Arial", 11), bg="white", width=15, anchor='w').pack(side='left')
        confirm_entry = tk.Entry(row3, font=("Arial", 11), show="*", width=25)
        confirm_entry.pack(side='left', padx=10)
        
        # Role
        row4 = tk.Frame(form_frame, bg="white")
        row4.pack(fill='x', pady=10)
        tk.Label(row4, text="Role:", font=("Arial", 11), bg="white", width=15, anchor='w').pack(side='left')
        role_var = tk.StringVar(value=user.get('role', 'employee'))
        role_combo = ttk.Combobox(row4, textvariable=role_var, values=["admin", "hr_manager", "employee"], width=23)
        role_combo.pack(side='left', padx=10)
        
        # Status
        row5 = tk.Frame(form_frame, bg="white")
        row5.pack(fill='x', pady=10)
        tk.Label(row5, text="Status:", font=("Arial", 11), bg="white", width=15, anchor='w').pack(side='left')
        status_var = tk.BooleanVar(value=user.get('is_active') == 1)
        tk.Checkbutton(row5, text="Active", variable=status_var, bg="white", font=("Arial", 11)).pack(side='left', padx=10)
        
        def save_edit():
            new_password = password_entry.get().strip()
            confirm = confirm_entry.get().strip()
            
            if new_password and new_password != confirm:
                messagebox.showerror("Error", "Passwords do not match")
                return
            
            # Update query
            if new_password:
                query = "UPDATE users SET password_hash = ?, role = ?, is_active = ? WHERE user_id = ?"
                params = (new_password, role_var.get(), 1 if status_var.get() else 0, user_id)
            else:
                query = "UPDATE users SET role = ?, is_active = ? WHERE user_id = ?"
                params = (role_var.get(), 1 if status_var.get() else 0, user_id)
            
            result = db.execute_command(query, params)
            
            if result is not None:
                messagebox.showinfo("Success", "User updated successfully!")
                dialog.destroy()
                self.load_users()
            else:
                messagebox.showerror("Error", "Failed to update user")
        
        btn_frame = tk.Frame(form_frame, bg="white")
        btn_frame.pack(pady=20)
        
        tk.Button(
            btn_frame,
            text="💾 Save Changes",
            font=("Arial", 11, "bold"),
            bg="#2ecc71",
            fg="white",
            padx=30,
            pady=8,
            command=save_edit
        ).pack(side='left', padx=10)
        
        tk.Button(
            btn_frame,
            text="❌ Cancel",
            font=("Arial", 11),
            bg="#95a5a6",
            fg="white",
            padx=30,
            pady=8,
            command=dialog.destroy
        ).pack(side='left', padx=10)
        
        dialog.grab_set()
        dialog.wait_window()

    def delete_user(self):
        """Delete selected user"""
        user_id = self.get_selected_user()
        if not user_id:
            return
        
        # Check if trying to delete own account
        if user_id == session.user_id:
            messagebox.showerror("Error", "You cannot delete your own account!")
            return
        
        # Confirm deletion
        if not messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this user?"):
            return
        
        # Delete user
        result = db.execute_command("DELETE FROM users WHERE user_id = ?", (user_id,))
        
        if result is not None:
            messagebox.showinfo("Success", "User deleted successfully!")
            self.load_users()
        else:
            messagebox.showerror("Error", "Failed to delete user")