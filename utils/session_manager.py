"""
session_manager.py - User Session Management
"""

import sys
import os

# Add main project path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class SessionManager:
    """Manage current user and session"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.current_user = None
            cls._instance.user_role = None
            cls._instance.user_id = None
        return cls._instance
    
    def login(self, user_data):
        """User login"""
        self.current_user = user_data
        self.user_id = user_data.get('user_id')
        self.user_role = user_data.get('role', 'employee')
        return True
    
    def logout(self):
        """User logout"""
        self.current_user = None
        self.user_role = None
        self.user_id = None
    
    def is_logged_in(self):
        """Check if user is logged in"""
        return self.current_user is not None
    
    def has_permission(self, permission):
        """Check user permission"""
        if not self.current_user:
            return False
        
        if self.user_role == 'admin':
            return True
        
        permissions = {
            'hr_manager': ['view_employees', 'add_employee', 'edit_employee', 'view_attendance'],
            'department_manager': ['view_employees', 'view_attendance', 'view_leaves'],
            'employee': ['view_own_profile', 'view_own_attendance', 'request_leave']
        }
        
        user_permissions = permissions.get(self.user_role, [])
        return permission in user_permissions
    
    def get_current_user(self):
        """Get current user data"""
        return self.current_user


# Create single instance
session = SessionManager()