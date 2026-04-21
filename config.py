"""
config.py - Project Configuration
"""

import os
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).parent
DATABASE_PATH = BASE_DIR / 'personnel.db'

# Application settings
APP_NAME = "Employee Management System"
APP_VERSION = "1.0.0"
COMPANY_NAME = "My Company"

# Payroll settings
SOCIAL_SECURITY_RATE = 0.075  # 7.5%
TAX_RATE = 0.10  # 10%
CURRENCY = "SAR"

# Leave types
LEAVE_TYPES = {
    'annual': 'Annual Leave',
    'sick': 'Sick Leave',
    'emergency': 'Emergency Leave',
    'unpaid': 'Unpaid Leave'
}

# Working hours
WORK_START_TIME = "09:00"
WORK_END_TIME = "17:00"
LATE_GRACE_MINUTES = 15