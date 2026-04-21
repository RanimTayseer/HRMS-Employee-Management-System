-- Create Database (SQLite - file is created automatically)
-- This file contains SQL commands to create tables

-- Departments Table
CREATE TABLE IF NOT EXISTS departments (
    department_id INTEGER PRIMARY KEY AUTOINCREMENT,
    department_code TEXT UNIQUE NOT NULL,
    department_name TEXT NOT NULL,
    description TEXT,
    manager_id INTEGER,
    is_active INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Activity Table
CREATE TABLE IF NOT EXISTS activities (
    activity_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    action TEXT,
    description TEXT,
    activity_type TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Employees Table
CREATE TABLE IF NOT EXISTS employees (
    employee_id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_number TEXT UNIQUE NOT NULL,
    full_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone TEXT,
    address TEXT,
    birth_date DATE,
    national_id TEXT UNIQUE,
    department_id INTEGER,
    position TEXT,
    employment_type TEXT DEFAULT 'full_time',
    basic_salary REAL NOT NULL,
    housing_allowance REAL DEFAULT 0,
    transport_allowance REAL DEFAULT 0,
    hire_date DATE NOT NULL,
    contract_end_date DATE,
    status TEXT DEFAULT 'active',
    profile_photo TEXT,
    user_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (department_id) REFERENCES departments(department_id)
);

-- Users Table (for login)
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    employee_id INTEGER UNIQUE,
    role TEXT DEFAULT 'employee',
    is_active INTEGER DEFAULT 1,
    last_login TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
);

-- Attendance Table
CREATE TABLE IF NOT EXISTS attendance (
    attendance_id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id INTEGER NOT NULL,
    date DATE NOT NULL,
    check_in TIME,
    check_out TIME,
    total_hours REAL DEFAULT 0,
    overtime_hours REAL DEFAULT 0,
    late_minutes INTEGER DEFAULT 0,
    status TEXT DEFAULT 'present',
    notes TEXT,
    created_by INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id),
    UNIQUE(employee_id, date)
);

-- Leaves Table
CREATE TABLE IF NOT EXISTS leaves (
    leave_id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id INTEGER,
    leave_type TEXT,
    start_date TEXT,
    end_date TEXT,
    days_count INTEGER,
    reason TEXT,
    status TEXT DEFAULT 'pending',
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

-- Payroll Table
CREATE TABLE IF NOT EXISTS payroll (
    payroll_id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id INTEGER NOT NULL,
    month TEXT NOT NULL,  -- Format: YYYY-MM
    basic_salary REAL NOT NULL,
    allowances REAL DEFAULT 0,
    overtime_amount REAL DEFAULT 0,
    bonus REAL DEFAULT 0,
    deductions REAL DEFAULT 0,
    net_salary REAL,
    payslip_path TEXT,
    paid_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id),
    UNIQUE(employee_id, month)
);

-- Audit Log Table
CREATE TABLE IF NOT EXISTS audit_log (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    action TEXT,
    table_name TEXT,
    record_id INTEGER,
    old_data TEXT,
    new_data TEXT,
    ip_address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Insert sample data (for testing)

-- Add default departments
INSERT OR IGNORE INTO departments (department_code, department_name, description) 
VALUES ('IT', 'Information Technology', 'IT and Software Department');

INSERT OR IGNORE INTO departments (department_code, department_name, description) 
VALUES ('HR', 'Human Resources', 'Employee Management Department');

INSERT OR IGNORE INTO departments (department_code, department_name, description) 
VALUES ('FIN', 'Finance', 'Accounting and Finance Department');

-- Add Admin user (password: admin123)
INSERT OR IGNORE INTO users (username, password_hash, role) 
VALUES ('admin', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.VT5JPq5pQq6bSK', 'admin');
-- Note: The encrypted password above is "admin123"