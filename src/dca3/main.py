"""
DCA3 Main Entry Point
Semiconductor Wafer Handling System with HSMS/GEM Integration
"""
import tkinter as tk
import sys
from dca3.config.settings import load_settings
from dca3.utils.logging import setup_logging

def main():
    """Main application entry point."""
    # Setup structured logging
    setup_logging()
    
    settings = load_settings()
    
    print("=" * 60)
    print("🚀 DCA3 Semiconductor Handling System Starting...")
    print(f"Mode: {'🧪 SIMULATION' if settings.simulation_mode else '🔴 LIVE'}")
    print(f"HSMS Mode: {settings.hsms_mode} | Port: {settings.hsms_port}")
    print("=" * 60)

    try:
        from dca3.ui.main_window import MainWindow
        
        root = tk.Tk()
        root.title("DCA3 - Semiconductor Wafer Handling System")
        root.geometry("1400x900")
        
        app = MainWindow(root, settings)
        root.mainloop()
        
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()