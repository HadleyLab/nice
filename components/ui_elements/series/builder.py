from nicegui import ui
import asyncio
from ..base.builder import BaseBuilder
from .config import SeriesConfig

class SeriesBuilder(BaseBuilder):
    """Builder for task series with reactive state management"""
    def __init__(self, config: SeriesConfig):
        super().__init__(config)
        self.config: SeriesConfig = config
        self._icon_name = self.config.status_icon or 'hourglass_empty'
        self.progress_state = None  # Will be initialized in build()

    @property
    def icon_name(self):
        return self._icon_name

    @icon_name.setter
    def icon_name(self, value):
        self._icon_name = value
        self.build.refresh()

    @ui.refreshable
    def build(self) -> ui.element:
        """Construct a series container with reactive buttons"""
        if not self.progress_state:
            self.progress_state, self.set_progress = ui.state({'value': 0.0})  # Proper tuple unpacking
        with ui.column() as container:
            # Header (root UI context)
            with ui.row().classes('items-center gap-4') as header:
                ui.icon(self.icon_name).classes('animate-spin')
                ui.label(self.config.series_name).classes('text-xl')
                
            # Reactive progress bar
            with ui.linear_progress().bind_value_from(self.progress_state, 'value'):
                pass  # Proper value binding from state
            
            # Button grid
            with ui.grid(columns=2).classes(self.config.spacing):
                for btn_config in self.config.buttons:
                    from components.ui_elements.button.builder import ButtonBuilder
                    button = ButtonBuilder(btn_config).build()
                    
            # Run all button
            if self.config.enable_run_all:
                with ui.row().classes('mt-4'):
                    ui.button(self.config.run_all_label,
                             icon=self.config.run_all_icon,
                             on_click=lambda: self.run_all_tasks())
        
        return container
        
    async def run_all_tasks(self):
        """Execute all tasks in sequence with proper async handling"""
        self.config.log("Starting all tasks in series", 'info')
        self.icon_name = 'hourglass_empty'
        self.set_progress({'value': 0.0})  # Use state setter function

        total_tasks = len(self.config.buttons)
        for idx, btn_config in enumerate(self.config.buttons, start=1):
            if not btn_config.validate():
                self.config.log("Validation failed - aborting series", 'error')
                return
                
            btn_config.loading_state.set(True)
            self.config.log(f"Starting task {btn_config.uid}", 'debug')
            
            # Simulate async task execution
            await asyncio.sleep(1.0)
            btn_config.loading_state.set(False)
            self.set_progress({'value': idx / total_tasks})  # Use state setter
            self.config.log(f"Completed task {btn_config.uid}", 'success')

        self.icon_name = 'check_circle'
        self.config.log("All series tasks completed successfully", 'success')
