from enum import Enum
from pydantic import BaseModel

class Color(str, Enum):
    """Mirror of NiceGUI's color palette with additional semantic meanings"""
    PRIMARY = 'primary'
    SECONDARY = 'secondary'
    ACCENT = 'accent'
    POSITIVE = 'positive'
    NEGATIVE = 'negative'
    WARNING = 'warning'
    INFO = 'info'
    DARK = 'dark'
    LIGHT = 'light'
    TRANSPARENT = 'transparent'
    
    # Semantic mappings
    SUCCESS = POSITIVE
    ERROR = NEGATIVE
    ALERT = WARNING

class BaseConfig(BaseModel):
    """Base configuration model for UI elements"""
    label: str = "Button"
    color: str = Color.PRIMARY
    state: str = "default"
    
    def update_state(self, new_state: str):
        """Safely update state with validation"""
        if new_state in ['active', 'completed', 'error', 'default']:
            self.state = new_state
    
    class Config:
        use_enum_values = True

class SeverityLevel(str, Enum):
    """Standardized severity levels mapped to NiceGUI colors"""
    INFO = 'info'
    SUCCESS = 'positive'
    WARNING = 'warning'
    ERROR = 'negative'
    DEFAULT = 'primary'
