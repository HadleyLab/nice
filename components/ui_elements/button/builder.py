import random
import traceback
import asyncio
import time
from nicegui import ui, app, run
from ..base.builder import BaseBuilder
from .config import ButtonConfig, SeverityLevel

class ButtonBuilder(BaseBuilder):
    """Builder for interactive button components"""
    
    def __init__(self, config: ButtonConfig):
        super().__init__(config)
        self.btn = None
        
    def build(self):
        """Construct the button element"""
        super().build()
        self.btn = ui.button(self.config.task_name)\
            .props(f'icon={self.config.default_icon} color={self.config.severity}')
        self._setup_handlers()
        return self.container
        
    def _setup_handlers(self):
        """Configure click handlers and animations"""
        self.btn.on_click(self._handle_click)
        
    @staticmethod
    def _simulate_failure(task_id: int):
        """Simulate processing time and potential failure"""
        time.sleep(0.3 + random.random())  # Varied processing time
        if random.random() < 0.1667:  # ~1/6 chance to fail
            raise ValueError(f"Task {task_id} failed randomly")
        return True

    async def _handle_click(self, event=None):
        """Handle button click with proper state management"""
        self.btn.props(f'icon={self.config.active_icon} color=primary')
        self.btn.loading = True
        ui.notify(f"Starting: {self.config.task_name}", 
                type=self.config.severity,
                clearable=True,
                timeout=self.config.notification_duration)
        
        async def execute_task():
            try:
                # Properly handle synchronous operation
                await run.cpu_bound(
                    ButtonBuilder._simulate_failure,
                    0  # Pass a default task ID for single button
                )
                
                self.btn.props(f'icon={self.config.completion_icon} color=positive')
                self.btn.loading = False
                ui.notify(f"Completed: {self.config.task_name}", 
                        type='positive',
                        clearable=True,
                        timeout=self.config.notification_duration)
                
                timer_complete = False
                
                def on_timer():
                    nonlocal timer_complete
                    timer_complete = True
                
                ui.timer(0.3, on_timer)
                while not timer_complete:
                    await asyncio.sleep(0.01)
                
                self.btn.props(f'icon={self.config.default_icon} color={self.config.severity}')
                
            except Exception as e:
                traceback.print_exc()  # Log full error to console
                severity = BaseConfig.get_severity(e)
                message = f"Failed: {self.config.task_name}"
                if hasattr(e, "message"):
                    message += f" - {e.message}"
                
                self.btn.props(f'color={severity.value} icon=error')
                self.btn.loading = False
                ui.notify(message,
                        type=severity.value,
                        clearable=True,
                        timeout=self.config.default_notification_duration)
        
        await execute_task()
