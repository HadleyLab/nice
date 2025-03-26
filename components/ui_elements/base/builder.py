from nicegui import ui
from .config import BaseConfig

class BaseBuilder:
    """Base class for UI element builders with reactive state management"""
    def __init__(self, config: BaseConfig):
        self.config = config
        self.element = None
        
    def build(self) -> ui.element:
        """Main construction method to be implemented by subclasses"""
        raise NotImplementedError("Subclasses must implement build()")
        
    def create_task_button(self, uid: str, label: str) -> ui.button:
        """Create a reactive task button with state management"""
        btn = ui.button(label)\
            .props(f'icon={self.config.icon.value}')\
            .classes('q-mb-sm')
            
        btn.on('click', lambda: self._handle_button_click(uid))
        return btn
        
    def _handle_button_click(self, uid: str):
        """Handle button click with integrated logging and state management"""
        self.config.log(f"Initializing task {uid}", 'debug')
        
        if not self.config.validate():
            return  # Validation errors already logged in config
            
        self.config.loading_state.value = True
        try:
            self.config.log(f"Task {uid} executing", 'info')
            # TODO: Implement actual task execution
            self.config.log(f"Task {uid} completed successfully", 'success')
        except Exception as e:
            self.config.log(f"Task {uid} failed: {str(e)}", 'error')
            raise
        finally:
            self.config.loading_state.value = False
            self.config.log(f"Task {uid} cleanup completed", 'debug')
