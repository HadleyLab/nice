from nicegui import ui
from .config import BaseConfig

class BaseBuilder:
    """Base class for UI element builders"""
    
    def __init__(self, config: BaseConfig):
        self.config = config
        self.container = ui.element('div')
        
    def build(self):
        """Base build method that should be overridden"""
        return self.container
        
    def update_state(self):
        """Update visual state based on configuration changes"""
        raise NotImplementedError("Subclasses must implement update_state")
