from nicegui import ui
from enum import Enum

class SeverityLevel(str, Enum):
    DEBUG = 'debug'
    INFO = 'info'
    WARNING = 'warning'
    ERROR = 'error'
    SUCCESS = 'success'

class BaseConfig:
    """Base configuration for UI elements using NiceGUI's reactive system"""
    def __init__(self, task_id: str = ''):
        self.task_id = task_id  # Non-reactive identifier
        self.label = ''         # Display label
        self.color = 'primary'  # UI color scheme
        self.status = 'default' # Current state
        self.log_level = 'info' # Default logging level
        self.log_messages = []  # Message history

    def __post_init__(self):
        """Validate required fields after initialization"""
        if not self.task_id:
            raise ValueError("task_id is required for BaseConfig")
        
    def validate(self):
        """Base validation method to be overridden"""
        if not self.task_id:
            ui.notify("Task ID is required", type='negative')
            return False
        return True

    def log(self, message: str, level: str = 'info'):
        """Unified logging with UI notifications"""
        ui.notify(message, type={
            'debug': 'info',
            'info': 'info',
            'warning': 'warning',
            'error': 'negative',
            'success': 'positive'
        }.get(level, 'info'))
