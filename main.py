"""VIKA Main Runner Script.

Run this script to start the local web server:
    python main.py
or:
    python app.py

Author: Abu Ziyad Al Katani (zydalz)
"""

import sys
import uvicorn
from src.config import SERVER_HOST, SERVER_PORT

if __name__ == "__main__":
    print(f"==================================================")
    print(f"   VIKA - Asisten Akademik Universitas Pamulang   ")
    print(f"   By: Abu Ziyad Al Katani (zydalz)              ")
    print(f"   Server running at: http://localhost:{SERVER_PORT}    ")
    print(f"==================================================")
    uvicorn.run("app:app", host=SERVER_HOST, port=SERVER_PORT, reload=True)
