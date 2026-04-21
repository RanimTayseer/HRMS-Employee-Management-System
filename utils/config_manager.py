"""
config_manager.py - Configuration Manager for Theme and Language
"""

import json
import os


class ConfigManager:
    """Manage application settings (theme, language, etc.)"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.config_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'app_config.json')
            cls._instance.config = cls._instance.load_config()
        return cls._instance
    
    def load_config(self):
        """Load configuration from file"""
        default_config = {
            'theme': 'light',  # light, dark, blue
            'language': 'english',  # english, arabic
            'items_per_page': 50,
            'date_format': 'YYYY-MM-DD'
        }
        
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    # Merge with default
                    for key, value in default_config.items():
                        if key not in config:
                            config[key] = value
                    return config
            except:
                return default_config
        return default_config
    
    def save_config(self):
        """Save configuration to file"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False
    
    def get(self, key, default=None):
        """Get configuration value"""
        return self.config.get(key, default)
    
    def set(self, key, value):
        """Set configuration value"""
        self.config[key] = value
        return self.save_config()
    
    def get_theme_colors(self):
        """Get theme colors based on current theme"""
        themes = {
            'light': {
                'bg': '#f0f4f8',
                'fg': '#2c3e50',
                'primary': '#1e5799',
                'secondary': '#3498db',
                'success': '#2ecc71',
                'danger': '#e74c3c',
                'warning': '#f39c12',
                'light': '#ecf0f1',
                'dark': '#2c3e50',
                'white': '#ffffff',
                'card_bg': '#ffffff',
                'sidebar_bg': '#ecf0f1',
                'header_bg': '#1e5799',
                'entry_bg': '#ffffff',
                'button_bg': '#3498db'
            },
            'dark': {
                'bg': '#1e1e2e',
                'fg': '#cdd6f4',
                'primary': '#89b4fa',
                'secondary': '#89b4fa',
                'success': '#a6e3a1',
                'danger': '#f38ba8',
                'warning': '#f9e2af',
                'light': '#313244',
                'dark': '#1e1e2e',
                'white': '#181825',
                'card_bg': '#313244',
                'sidebar_bg': '#181825',
                'header_bg': '#11111b',
                'entry_bg': '#313244',
                'button_bg': '#89b4fa'
            },
            'blue': {
                'bg': '#e8f4f8',
                'fg': '#1a3a5c',
                'primary': '#1e88e5',
                'secondary': '#42a5f5',
                'success': '#43a047',
                'danger': '#e53935',
                'warning': '#fb8c00',
                'light': '#e3f2fd',
                'dark': '#1565c0',
                'white': '#ffffff',
                'card_bg': '#ffffff',
                'sidebar_bg': '#bbdefb',
                'header_bg': '#1e88e5',
                'entry_bg': '#ffffff',
                'button_bg': '#1e88e5'
            }
        }
        
        return themes.get(self.get('theme', 'light'), themes['light'])
    
    def get_text(self, key):
        """Get translated text"""
        texts = {
            'english': {
                # General
                'app_title': 'Employee Management System',
                'dashboard': 'Dashboard',
                'employees': 'Employees',
                'departments': 'Departments',
                'attendance': 'Attendance',
                'leaves': 'Leaves',
                'payroll': 'Payroll',
                'reports': 'Reports',
                'settings': 'Settings',
                'logout': 'Logout',
                'login': 'Login',
                'username': 'Username',
                'password': 'Password',
                'error': 'Error',
                'success': 'Success',
                'warning': 'Warning',
                'confirm': 'Confirm',
                'save': 'Save',
                'cancel': 'Cancel',
                'delete': 'Delete',
                'edit': 'Edit',
                'add': 'Add',
                'search': 'Search',
                'refresh': 'Refresh',
                'export': 'Export',
                'backup': 'Backup',
                'restore': 'Restore',
                
                # Dashboard
                'total_employees': 'Total Employees',
                'total_departments': 'Total Departments',
                'today_attendance': "Today's Attendance",
                'pending_leaves': 'Pending Leaves',
                
                # Settings
                'general_settings': 'General Settings',
                'company_settings': 'Company Settings',
                'payroll_settings': 'Payroll Settings',
                'backup_settings': 'Backup Settings',
                'users_settings': 'Users Settings',
                'language': 'Language',
                'theme': 'Theme',
                'light_theme': 'Light',
                'dark_theme': 'Dark',
                'blue_theme': 'Blue',
                'company_name': 'Company Name',
                'company_address': 'Company Address',
                'company_phone': 'Company Phone',
                'company_email': 'Company Email',
                'working_hours': 'Working Hours per Day',
                'overtime_rate': 'Overtime Rate',
                'currency': 'Currency'
            },
            'arabic': {
                # General
                'app_title': 'نظام إدارة شؤون الموظفين',
                'dashboard': 'الرئيسية',
                'employees': 'الموظفين',
                'departments': 'الأقسام',
                'attendance': 'الحضور',
                'leaves': 'الإجازات',
                'payroll': 'الرواتب',
                'reports': 'التقارير',
                'settings': 'الإعدادات',
                'logout': 'تسجيل خروج',
                'login': 'تسجيل الدخول',
                'username': 'اسم المستخدم',
                'password': 'كلمة المرور',
                'error': 'خطأ',
                'success': 'نجاح',
                'warning': 'تنبيه',
                'confirm': 'تأكيد',
                'save': 'حفظ',
                'cancel': 'إلغاء',
                'delete': 'حذف',
                'edit': 'تعديل',
                'add': 'إضافة',
                'search': 'بحث',
                'refresh': 'تحديث',
                'export': 'تصدير',
                'backup': 'نسخ احتياطي',
                'restore': 'استعادة',
                
                # Dashboard
                'total_employees': 'عدد الموظفين',
                'total_departments': 'عدد الأقسام',
                'today_attendance': 'حضور اليوم',
                'pending_leaves': 'إجازات معلقة',
                
                # Settings
                'general_settings': 'الإعدادات العامة',
                'company_settings': 'بيانات الشركة',
                'payroll_settings': 'إعدادات الرواتب',
                'backup_settings': 'النسخ الاحتياطي',
                'users_settings': 'إدارة المستخدمين',
                'language': 'اللغة',
                'theme': 'المظهر',
                'light_theme': 'فاتح',
                'dark_theme': 'داكن',
                'blue_theme': 'أزرق',
                'company_name': 'اسم الشركة',
                'company_address': 'عنوان الشركة',
                'company_phone': 'هاتف الشركة',
                'company_email': 'بريد الشركة',
                'working_hours': 'ساعات العمل اليومية',
                'overtime_rate': 'نسبة العمل الإضافي',
                'currency': 'العملة'
            }
        }
        
        lang = self.get('language', 'english')
        return texts.get(lang, texts['english']).get(key, key)


# Create single instance
config = ConfigManager()