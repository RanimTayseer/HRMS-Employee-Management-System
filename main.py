"""
main.py - Application Entry Point
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("✅ Starting application...")

try:
    from views.login_window import LoginWindow
    print("✅ LoginWindow imported successfully")
    
    print("✅ Opening login window...")
    app = LoginWindow()
    app.run()
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    input("Press Enter to exit...")