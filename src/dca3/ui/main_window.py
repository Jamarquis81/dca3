"""
DCA3 Main Window - Updated with HSMS integration
"""
import tkinter as tk
from tkinter import ttk
import threading
from dca3.config.settings import Settings
from dca3.comms.hsms_manager import HSMSManager

class MainWindow:
    def __init__(self, root: tk.Tk, settings: Settings):
        self.root = root
        self.settings = settings
        self.hsms_manager = HSMSManager(settings)

        # GEM Handler
        from dca3.comms.gem_handler import GemHandler
        self.gem_handler = GemHandler(settings, self.hsms_manager)
        
        self.root.title("DCA3 - Semiconductor Wafer Handling System")
        self.root.geometry("1450x920")
        
        self.setup_ui()
        self.hsms_manager.register_callback(self.on_hsms_status_change)
        self.log("✅ DCA3 UI Started - Simulation Mode Active")

    def setup_ui(self):
        # Top Toolbar
        toolbar = ttk.Frame(self.root, padding=10)
        toolbar.pack(fill="x")
        
        ttk.Label(toolbar, text="DCA3", font=("Arial", 18, "bold")).pack(side="left")
        ttk.Label(toolbar, text="Semiconductor Handling System", font=("Arial", 11)).pack(side="left", padx=10)
        
        # HSMS Controls
        ctrl_frame = ttk.Frame(toolbar)
        ctrl_frame.pack(side="right")
        
        ttk.Button(ctrl_frame, text="Enable HSMS", command=self.enable_hsms).pack(side="left", padx=5)
        ttk.Button(ctrl_frame, text="Disable HSMS", command=self.disable_hsms).pack(side="left", padx=5)
        ttk.Button(ctrl_frame, text="GEM Status", command=self.show_gem_status).pack(side="left", padx=5)

        self.hsms_status = ttk.Label(ctrl_frame, text="HSMS: Disconnected", foreground="red")
        self.hsms_status.pack(side="left", padx=15)

        # Main Panes (same as before)
        main_pane = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        main_pane.pack(fill="both", expand=True, padx=10, pady=5)

        # Left Cassettes
        left = ttk.LabelFrame(main_pane, text="Cassettes", width=280)
        ttk.Label(left, text="Port A\n[Sim]").pack(pady=40)
        ttk.Label(left, text="Port B\n[Sim]").pack(pady=40)
        main_pane.add(left)

        # Center
        center = ttk.LabelFrame(main_pane, text="Robot & Wafer Map")
        ttk.Label(center, text="Robot Control Area\n\nSimulation Running", font=("Arial", 12)).pack(expand=True)
        main_pane.add(center, weight=2)

        # Right
        right = ttk.LabelFrame(main_pane, text="Camera + GEM")
        ttk.Label(right, text="Camera View\n[Simulation]\n\nGEM Status").pack(expand=True)
        main_pane.add(right)

        # Bottom Log
        log_frame = ttk.LabelFrame(self.root, text="Log Console", height=220)
        log_frame.pack(fill="x", padx=10, pady=5)
        self.log_text = tk.Text(log_frame, height=12, font=("Consolas", 10))
        self.log_text.pack(fill="both", expand=True, padx=5, pady=5)

    def enable_hsms(self):
        self.log("Enabling HSMS connection...")
        threading.Thread(target=self.hsms_manager.enable, daemon=True).start()

    def disable_hsms(self):
        self.hsms_manager.disable()
        self.log("HSMS disabled")

    def on_hsms_status_change(self, connected: bool):
        if connected:
            self.hsms_status.config(text="HSMS: Connected", foreground="green")
            self.log("✅ HSMS Connected Successfully")
        else:
            self.hsms_status.config(text="HSMS: Disconnected", foreground="red")

    def show_gem_status(self):
        status = self.gem_handler.get_status_report()
        msg = f"GEM Status:\nControl: {status['control_state']}\n"
        msg += f"Active Alarms: {status['active_alarms']}\n"
        msg += f"Spooled Events: {status['spooled_count']}"
        self.log(msg)

    def test_gem_event(self):
        self.gem_handler.report_event(1003, "Robot Move Complete - Test")
        self.log("GEM Event triggered: Robot Move Complete")

        
    def log(self, message: str):
        timestamp = "→ "
        self.log_text.insert("end", f"{timestamp}{message}\n")
        self.log_text.see("end")

