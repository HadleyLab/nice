from ..base.config import BaseConfig
from nicegui import ui

class ButtonConfig(BaseConfig):
    """Button configuration using native NiceGUI reactivity"""
    def __init__(self, 
                 task_id: str = '',
                 default_icon: str = 'play_circle',
                 active_icon: str = 'hourglass_empty',
                 completion_icon: str = 'check_circle',
                 severity: str = 'primary',
                 notification_duration: float = 2.5):
        super().__init__(task_id)
        self.icon = default_icon
        self.default_icon = default_icon
        self.active_icon = active_icon
        self.completion_icon = completion_icon
        self.severity = severity
        self.loading = False
        self.notification_duration = notification_duration

    def __post_init__(self):
        """Validate after initialization"""
        super().__post_init__()

    def validate(self):
        """Simplified validation using native reactivity"""
        return super().validate() and bool(self.label)
