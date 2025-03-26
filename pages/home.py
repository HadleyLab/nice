from components.ui_elements.button.config import ButtonConfig
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
            task_name="Single Task",
            initial_color="green",
            success_icon="task_alt"
        )
        button_builder = ButtonBuilder(single_config)
        button_builder.build()
        
        # Series demo
        series_config = SeriesConfig(
            series_name="Task Series",
            buttons=[
                ButtonConfig(task_name="First Task"),
                ButtonConfig(task_name="Second Task", initial_color="purple"),
                ButtonConfig(task_name="Third Task", log_severity="WARNING")
            ],
            layout="row",
            spacing="gap-8"
        )
        series_builder = SeriesBuilder(series_config)
        series_builder.build()
