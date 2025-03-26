from dataclasses import dataclass

@dataclass
class BaseConfig:
    """Base configuration class for UI elements"""
    uid: str
    style: dict = None
    
    def __init__(self, uid: str, style: dict = None):
        self.uid = uid
        self.style = style or {}
        
    def validate(self):
        """Validate configuration settings"""
        if not self.uid:
            raise ValueError("UID is required for all UI elements")
