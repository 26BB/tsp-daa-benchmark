import sys
import os

# Delegate directly to src/app.py
app_path = os.path.join(os.path.dirname(__file__), "src", "app.py")
with open(app_path, "r", encoding="utf-8") as f:
    code = f.read()
exec(code)
