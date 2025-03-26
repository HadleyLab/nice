from nicegui import ui
from .config import BaseConfig

class BaseLayout:
    """Core layout manager implementing full context manager protocol"""
    def __init__(self):
        self.content_container = None
        
    def __enter__(self):
        # Create header
        with ui.header().classes('items-center justify-between bg-blue-100') as self.header:
            ui.label('App Builder').classes('text-2xl font-bold')
            ui.button(icon='menu').props('flat')
            
        # Create main content container
        self.content_container = ui.column().classes('w-full p-4')
        
        # Create footer
        with ui.footer().classes('bg-gray-100 p-2 justify-center'):
            ui.label('© 2024 Your Company Name').classes('text-sm text-gray-600')
            
        return self.content_container
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass  # Context cleanup handled by NiceGUI

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
