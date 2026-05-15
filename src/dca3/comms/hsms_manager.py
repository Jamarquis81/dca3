"""
HSMS Manager for DCA3 - Simulation Mode (Real HSMS coming soon)
"""
from typing import Callable
from dca3.config.settings import Settings
import structlog
import time
import threading

logger = structlog.get_logger(__name__)

class HSMSManager:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.connected = False
        self._callbacks = []
        self._sim_thread = None

    def enable(self):
        """Simulate HSMS connection (for development)"""
        if self.connected:
            return

        try:
            logger.info("Starting HSMS in SIMULATION mode")
            
            # Simulate connection delay
            time.sleep(0.8)
            
            self.connected = True
            logger.info("✅ HSMS SIMULATION Connected", 
                       ip=self.settings.hsms_ip, 
                       port=self.settings.hsms_port)
            
            self._notify_callbacks(True)
            
            # Optional: Simulate some traffic
            self._start_simulation_traffic()
            
        except Exception as e:
            logger.error("Failed to enable HSMS sim", error=str(e))

    def _start_simulation_traffic(self):
        """Simulate periodic GEM events"""
        def traffic():
            while self.connected:
                time.sleep(8)
                try:
                    logger.info("SIM: S6F11 - Event Report (Wafer Processed)")
                except:
                    break
        self._sim_thread = threading.Thread(target=traffic, daemon=True)
        self._sim_thread.start()

    def disable(self):
        """Disable HSMS"""
        self.connected = False
        logger.info("HSMS Simulation disabled")
        self._notify_callbacks(False)

    def register_callback(self, callback: Callable):
        self._callbacks.append(callback)

    def _notify_callbacks(self, connected: bool):
        for cb in self._callbacks:
            try:
                cb(connected)
            except:
                pass

    def send_test_message(self):
        logger.info("SIM: S1F1 Are You There sent (simulated)")