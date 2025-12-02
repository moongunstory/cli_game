#!/usr/bin/env python3
"""
Monster Evolution RPG - Python Launcher Wrapper
Alternative way to run the game: python run_game.py
"""

import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import and run the main game
from cli_game.main import main

if __name__ == "__main__":
    main()
