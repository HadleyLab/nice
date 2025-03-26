from nicegui import ui
from ..base.config import BaseConfig, SeverityLevel

class SeriesConfig(BaseConfig):
    """Reactive configuration for task series"""
    def __init__(self, 
                 series_name: str = '',
                 buttons: list = None,
                 spacing: str = 'gap-4',
                 layout: str = 'column',
                 completion_icon: str = 'done_all',
                 log_severity: str = 'positive',
                 enable_run_all: bool = True,
                 run_all_label: str = 'Run All Tasks',
                 run_all_severity: str = 'primary',
                 run_all_icon: str = 'play_arrow',
                 run_all_completion_icon: str = 'check_circle',
                 progress_color: str = 'primary',
                 status_type: str = 'ongoing',
                 status_icon: str = 'rotate_right',
                 notification_duration: float = 3.0,
                 progress: float = 0.0):
        super().__init__()
        self.series_name = series_name
        self.buttons = buttons or []
        self.spacing = spacing
        self.layout = layout
        self.completion_icon = completion_icon
        self.log_severity = log_severity
        self.enable_run_all = enable_run_all
        self.run_all_label = run_all_label
        self.run_all_severity = run_all_severity
        self.run_all_icon = run_all_icon
        self.run_all_completion_icon = run_all_completion_icon
        self.progress_color = progress_color
        self.status_type = status_type
        self.status_icon = status_icon
        self.notification_duration = notification_duration
        self.progress = progress
