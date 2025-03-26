from .config import SeriesConfig
from components.ui_elements.button.builder import ButtonBuilder
from nicegui import ui

class SeriesBuilder:
    """Constructs and manages a series of related UI tasks"""
    
    def __init__(self, config: SeriesConfig):
        self.config = config
        self.buttons = []
        
    def build(self):
        """Context manager for building the series"""
        self.container = ui.column().classes(f"{self.config.spacing} {self.config.layout}")
        with self.container:
            ui.label(self.config.series_name).classes("text-xl font-bold")
            for btn_config in self.config.buttons:
                button = ButtonBuilder(btn_config)
                self.buttons.append(button)
                with button.build():
                    pass  # Button context handles its own rendering
        return self.container


    def delete(self):
        """Clean up all series components"""
        for btn in self.buttons:
            btn.delete()
        self.container.delete()

    def log_completion(self):
        """Log series completion"""
        ui.notify(
            f"Completed series '{self.config.series_name}'",
            type='positive',
            icon=self.config.completion_icon,
            timeout=self.config.buttons[0].notification_duration if self.config.buttons else 3000
        )
        ui.notify("Series completed!", icon=self.config.completion_icon)
