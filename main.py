from nicegui import ui, run, app
import asyncio
import yaml
import time

from components.configs.button_task_config import ButtonTaskConfig
from components.configs.button_task_series_config import ButtonTaskSeriesConfig
from components.builders.button_task_builder import ButtonTaskBuilder
from components.builders.button_task_series_builder import ButtonTaskSeriesBuilder



# ---------- Demo Setup ----------
def configure_demo():
    """Simplified demo showing core functionality"""
    # Initialize app state storage
    if not hasattr(app.state, 'tasks'):
        app.state.tasks = {}
        
    # Create task builders with default config
    task_builders = {
        f"task{i}": ButtonTaskBuilder(ButtonTaskConfig(task_name=f"Task {i}"), f"task{i}")
        for i in range(1, 7)
    }
    
    # Create series configuration
    series_config = ButtonTaskSeriesConfig(
        series_name="Demo Series",
        tasks=list(task_builders.keys()),
        show_progress=True
    )
    
    # Build UI components
    with ui.column().classes("w-full max-w-2xl gap-6 p-8 bg-white rounded-lg shadow-lg"):
        # Display individual task buttons
        for builder in task_builders.values():
            builder.container.classes("w-full")
            builder.btn.classes("w-full py-4")
            
        # Add series controls
        series_builder = ButtonTaskSeriesBuilder(series_config, task_builders)
        series_builder.container.classes("w-full")
        if series_builder.config.show_progress and hasattr(series_builder, 'progress_bar'):
            series_builder.progress_bar.classes("w-full")
        
@ui.page('/')
def main_page():
    configure_demo()

if __name__ in {"__main__", "__mp_main__"}:
    ui.run(host='0.0.0.0', port=8080, show=False)
