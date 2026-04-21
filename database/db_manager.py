"""
db_manager.py - Database Manager
"""

import sqlite3
import os
from pathlib import Path
import sys

# Add main project path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class DatabaseManager:
    """Database Controller"""
    
    def __init__(self, db_path=None):
        """Initialize database manager"""
        if db_path is None:
            # Set database path
            self.db_path = Path(__file__).parent.parent / 'personnel.db'
        else:
            self.db_path = Path(db_path)
        
        self.connection = None
        self.cursor = None
        
    def connect(self):
        """Create database connection"""
        try:
            self.connection = sqlite3.connect(str(self.db_path))
            self.connection.row_factory = sqlite3.Row
            self.cursor = self.connection.cursor()
            return True
        except Exception as e:
            print(f"Database connection error: {e}")
            return False
    
    def disconnect(self):
        """Close connection"""
        if self.connection:
            self.connection.close()
            self.connection = None
            self.cursor = None
    
    def execute_query(self, query, params=None):
        """Execute SELECT query"""
        try:
            if not self.connection:
                self.connect()
            
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            
            results = self.cursor.fetchall()
            return [dict(row) for row in results]
        except Exception as e:
            print(f"Query error: {e}")
            return []
    
    def execute_command(self, query, params=None):
        """Execute INSERT, UPDATE, DELETE command"""
        try:
            if not self.connection:
                self.connect()
            
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            
            self.connection.commit()
            return self.cursor.lastrowid
        except Exception as e:
            print(f"Command execution error: {e}")
            if self.connection:
                self.connection.rollback()
            return None
    
    def get_table_count(self, table_name):
        """Get number of records in a table"""
        query = f"SELECT COUNT(*) as count FROM {table_name}"
        result = self.execute_query(query)
        return result[0]['count'] if result else 0


# Create single instance for use everywhere
db = DatabaseManager()