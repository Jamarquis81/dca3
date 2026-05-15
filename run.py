#!/usr/bin/env python3
"""
DCA3 Semiconductor Handling System - Easy Launcher
"""
import os
import sys

# Add src directory to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(project_root, "src")
sys.path.insert(0, src_path)

if __name__ == "__main__":
    try:
        from dca3.main import main
        main()
    except Exception as e:
        print(f"❌ Error starting DCA3: {e}")
        import traceback
        traceback.print_exc()
        input("Press Enter to exit...")