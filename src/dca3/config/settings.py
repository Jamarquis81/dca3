"""
DCA3 Configuration Settings using Pydantic
"""
from pydantic import BaseModel, Field
from typing import Literal
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseModel):
    # HSMS Settings
    hsms_mode: Literal["equipment", "host"] = Field(default="equipment")
    hsms_ip: str = Field(default="127.0.0.1")
    hsms_port: int = Field(default=5000)
    device_id: int = Field(default=1000)
    
    # Simulation
    simulation_mode: bool = Field(default=True)
    
    # Logging
    log_max_size_mb: int = Field(default=1)
    log_backup_count: int = Field(default=30)

def load_settings() -> Settings:
    """Load settings from environment variables."""
    return Settings(
        hsms_mode=os.getenv("HSMS_MODE", "equipment"),
        hsms_ip=os.getenv("HSMS_IP", "127.0.0.1"),
        hsms_port=int(os.getenv("HSMS_PORT", "5000")),
        device_id=int(os.getenv("DEVICE_ID", "1000")),
        simulation_mode=os.getenv("SIMULATION_MODE", "true").lower() == "true",
    )