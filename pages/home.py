from components.ui_elements.button.config import ButtonConfig
from components.ui_elements.base.config import SeverityLevel
from components.ui_elements.button.builder import ButtonBuilder
from components.ui_elements.series.config import SeriesConfig
from components.ui_elements.series.builder import SeriesBuilder
from nicegui import ui, app

def create():
    """Home page with component demos"""
    with ui.column().classes("w-full p-8 gap-8"):
        ui.label("Component Demo").classes("text-3xl font-bold")
        
        # Single button demo
        single_config = ButtonConfig(
            task_id="single_task",
            default_icon="play_arrow",
            severity='success'
        )
        button_builder = ButtonBuilder(single_config)
        button_builder.build()
        
        # Series demo
        series_config = SeriesConfig(
            series_name="Task Series",
            buttons=[
                ButtonConfig(task_id="task1", severity='info'),
                ButtonConfig(task_id="task2", severity='warning'),
                ButtonConfig(task_id="task3", severity='error')
            ],
            log_severity=SeverityLevel.INFO,
            layout="row", 
            spacing="gap-8",
            enable_run_all=True
        )
        series_builder = SeriesBuilder(series_config)
        series_builder.build()
