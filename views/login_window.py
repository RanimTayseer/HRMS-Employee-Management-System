"""
login_window.py - Login Window
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

# Add main project path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import bcrypt
from database.db_manager import db
from utils.session_manager import session


class LoginWindow:
    """Login Window"""
    
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Employee Management System - Login")
        self.window.geometry("500x400")
        self.window.resizable(False, False)
        
        # Set colors
        self.bg_color = "#f0f0f0"
        self.primary_color = "#2c3e50"
        self.button_color = "#3498db"
        
        self.window.configure(bg=self.bg_color)
        
        self.setup_ui()
        
    def setup_ui(self):
        """Create user interface"""
        
        # Main frame
        main_frame = tk.Frame(self.window, bg=self.bg_color)
        main_frame.pack(expand=True, fill='both', padx=40, pady=40)
        
        # Program title
        title_label = tk.Label(
            main_frame, 
            text="Employee Management System", 
            font=("Arial", 24, "bold"),
            bg=self.bg_color,
            fg=self.primary_color
        )
        title_label.pack(pady=(0, 30))
        
        # White input frame
        input_frame = tk.Frame(main_frame, bg="white", relief=tk.RAISED, bd=1)
        input_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Username
        username_label = tk.Label(
            input_frame, 
            text="Username:", 
            font=("Arial", 12),
            bg="white"
        )
        username_label.pack(anchor='w', padx=20, pady=(20, 5))
        
        self.username_entry = tk.Entry(
            input_frame, 
            font=("Arial", 12),
            bd=1,
            relief=tk.SUNKEN
        )
        self.username_entry.pack(fill='x', padx=20, pady=(0, 15))
        self.username_entry.focus()
        
        # Password
        password_label = tk.Label(
            input_frame, 
            text="Password:", 
            font=("Arial", 12),
            bg="white"
        )
        password_label.pack(anchor='w', padx=20, pady=(0, 5))
        
        self.password_entry = tk.Entry(
            input_frame, 
            font=("Arial", 12),
            show="*",
            bd=1,
            relief=tk.SUNKEN
        )
        self.password_entry.pack(fill='x', padx=20, pady=(0, 20))
        
        # Login button
        self.login_button = tk.Button(
            input_frame,
            text="Login",
            font=("Arial", 12, "bold"),
            bg=self.button_color,
            fg="white",
            bd=0,
            padx=20,
            pady=10,
            cursor="hand2",
            command=self.login
        )
        self.login_button.pack(pady=(0, 20))
        
        # Bind Enter key to login button
        self.window.bind('<Return>', lambda event: self.login())
        
        # Footer message
        footer_label = tk.Label(
            main_frame,
            text="© 2024 - Employee Management System",
            font=("Arial", 8),
            bg=self.bg_color,
            fg="gray"
        )
        footer_label.pack(pady=(10, 0))
    
    def login(self):
        """Handle login process"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter username and password")
            return
        
        query = "SELECT * FROM users WHERE username = ? AND is_active = 1"
        result = db.execute_query(query, (username,))
        
        if not result:
            messagebox.showerror("Error", "Invalid username or password")
            return
        
        user = result[0]
        
        # Compare password (stored as plain text in database)
        if password == user.get('password_hash'):
            session.login(user)
            
            db.execute_command(
                "UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE user_id = ?",
                (user['user_id'],)
            )
            
            self.window.destroy()
            self.open_main_window()
        else:
            messagebox.showerror("Error", "Invalid username or password")
    
    def open_main_window(self):
        """Open main window"""
        from views.main_window import MainWindow
        main_window = MainWindow()
        main_window.run()
    
    def run(self):
        """Run the window"""
        self.window.mainloop()


# For direct testing
if __name__ == "__main__":
    app = LoginWindow()
    app.run()