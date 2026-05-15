# DCA3 Main Entry Point

import tkinter as tk
from dca3.ui.main_window import MainWindow
from dca3.comms.hsms_manager import HSMSManager
from dca3.config.paths import LOGS_DIR


def main():
    # Setup logging
    from dca3.utils.logging import logger
    logger.info("Starting DCA3 Semiconductor Handling System")

    # Initialize HSMS/GEM
    hsms = HSMSManager()
    # hsms.start()  # Will be enabled after full implementation

    # Create and run GUI
    root = tk.Tk()
    root.title("DCA3 - Semiconductor Wafer Handler")
    root.geometry("1200x800")

    app = MainWindow(root, hsms_manager=hsms)
    root.mainloop()


if __name__ == "__main__":
    main()
