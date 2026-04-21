from database.db_manager import db
from datetime import datetime

class ActivityModel:
    def __init__(self):
        self.db = db
    
    def add_activity(self, user_id, action, description, activity_type):
        query = """
        INSERT INTO activities (user_id, action, description, activity_type)
        VALUES (?, ?, ?, ?)
        """
        return self.db.execute_command(query, (user_id, action, description, activity_type))
    
    def get_recent_activities(self, limit=10):
        query = """
        SELECT a.*, u.username
        FROM activities a
        LEFT JOIN users u ON a.user_id = u.user_id
        ORDER BY a.created_at DESC
        LIMIT ?
        """
        return self.db.execute_query(query, (limit,))