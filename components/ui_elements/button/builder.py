from nicegui import ui
from ..base.builder import BaseBuilder
from .config import ButtonConfig

class ButtonBuilder(BaseBuilder):
    """Builder for interactive button components"""
    
    def __init__(self, config: ButtonConfig):
        super().__init__(config)
        self.btn = None
        
    def build(self):
        """Construct the button element"""
        super().build()
        self.btn = ui.button(self.config.task_name)
        self._setup_handlers()
        return self.container
        
    def _setup_handlers(self):
        """Configure click handlers and animations"""
        self.btn.on_click(self._handle_click)
        
    def _handle_click(self, event=None):
        """Handle button click with proper state management"""
        try:
            self.config.status = 'active'
            self.update_state()
            ui.notify(f"Starting: {self.config.task_name}", type='ongoing', color='blue')
            
            # Simulate task completion after delay
            def complete_task():
                self.config.status = 'completed'
                self.update_state()
                ui.notify(f"Completed: {self.config.task_name}", type='positive', color='green')
                
            ui.timer(2.0, complete_task, once=True)
            
        except Exception as e:
            self.config.status = 'error'
            self.update_state()
            ui.notify(f"Failed: {self.config.task_name} - {str(e)}", type='negative', color='red')
            print(f"ERROR: {self.config.task_name} - {str(e)}")  # Console logging
        
    def update_state(self):
        """Update visual state with proper styling"""
        color_map = {
            'active': 'bg-blue-500',
            'completed': 'bg-green-500',
            'error': 'bg-red-500'
        }
        self.btn.classes(replace=color_map.get(self.config.status, 'bg-gray-500'))
        self.btn.props(f'color={self.config.status}')
