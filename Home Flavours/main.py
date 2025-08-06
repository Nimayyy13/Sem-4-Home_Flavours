#!/usr/bin/env python3
"""
Home Flavours - Main Application Entry Point
Organized project structure with frontend, backend, and database folders
"""

import sys
import os

# Add the backend folder to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

# Import from organized structure
from frontend.simple_main import main

if __name__ == "__main__":
    main() 