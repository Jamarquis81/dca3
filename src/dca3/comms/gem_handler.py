"""
Full GEM (SEMI E30) Handler for DCA3
Supports: SVIDs, CEIDs, Alarms, Remote Commands, Control State, Spooling
"""
from typing import Dict, Any, List, Callable
from dca3.config.settings import Settings
import structlog
import time
import threading

logger = structlog.get_logger(__name__)

class GemHandler:
    def __init__(self, settings: Settings, hsms_manager):
        self.settings = settings
        self.hsms = hsms_manager
        self.control_state = "OFFLINE"          # OFFLINE, ONLINE LOCAL, ONLINE REMOTE
        self.active_alarms: Dict[int, str] = {}
        self.spooling_enabled = False
        self.spooled_events = []
        
        # Sample SVIDs (Status Variables)
        self.svids: Dict[int, Any] = {
            1: "DCA3-Simulator-v1.0",           # Model Name
            2: "v0.1.0",                        # Software Revision
            10: "IDLE",                         # Robot Status
            20: 0,                              # Wafers Processed
            21: 25,                             # Cassette A Slot Count
            22: 18,                             # Cassette B Slot Count
            30: "SIMULATION",                   # Operation Mode
            100: "ONLINE",                      # GEM Control State
        }

        # Sample CEIDs (Collection Events)
        self.ceids = {
            1001: "Wafer Loaded",
            1002: "Wafer Unloaded",
            1003: "Robot Move Complete",
            1004: "Inspection Complete",
            2001: "Alarm Triggered",
            3001: "Recipe Selected",
        }

        logger.info("GEM Handler initialized")

    def update_control_state(self, new_state: str):
        """Update GEM Control State"""
        valid_states = ["OFFLINE", "ONLINE LOCAL", "ONLINE REMOTE"]
        if new_state in valid_states:
            self.control_state = new_state
            self.svids[100] = new_state
            logger.info("GEM Control State changed", state=new_state)
            self.report_event(1005, f"Control State → {new_state}")

    def set_svid(self, svid: int, value: Any):
        """Update a Status Variable"""
        self.svids[svid] = value
        logger.info("SVID updated", svid=svid, value=value)

    def trigger_alarm(self, alarm_id: int, text: str):
        """Trigger an Alarm"""
        self.active_alarms[alarm_id] = text
        logger.warning("ALARM TRIGGERED", alarm_id=alarm_id, text=text)
        self.report_event(2001, f"Alarm {alarm_id}: {text}")

    def clear_alarm(self, alarm_id: int):
        """Clear an Alarm"""
        if alarm_id in self.active_alarms:
            del self.active_alarms[alarm_id]
            logger.info("Alarm cleared", alarm_id=alarm_id)

    def report_event(self, ceid: int, description: str = ""):
        """Report a Collection Event (with spooling support)"""
        event_name = self.ceids.get(ceid, f"Event_{ceid}")
        
        if self.hsms.connected:
            logger.info("GEM Event Reported", ceid=ceid, name=event_name, desc=description)
        else:
            if self.spooling_enabled:
                self.spooled_events.append((ceid, description))
                logger.info("Event Spooled", ceid=ceid)
            else:
                logger.info("GEM Event (not sent - disconnected)", ceid=ceid)

    def process_remote_command(self, command: str, params: Dict = None):
        """Handle Remote Commands from Host (S2F41)"""
        params = params or {}
        logger.info("Remote Command Received", command=command, params=params)

        if command == "START":
            self.report_event(3001, "Process Started")
        elif command == "STOP":
            self.report_event(3002, "Process Stopped")
        elif command == "PAUSE":
            self.update_control_state("ONLINE LOCAL")
        elif command == "RESUME":
            self.update_control_state("ONLINE REMOTE")
        elif command == "HOME_ROBOT":
            logger.info("Robot homing via remote command")
        else:
            logger.warning("Unknown remote command", command=command)

        return {"status": "OK", "command": command}

    def get_status_report(self) -> Dict:
        """Return current GEM status for UI"""
        return {
            "control_state": self.control_state,
            "active_alarms": len(self.active_alarms),
            "svids_count": len(self.svids),
            "spooling": self.spooling_enabled,
            "spooled_count": len(self.spooled_events)
        }