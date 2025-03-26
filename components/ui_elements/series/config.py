from dataclasses import dataclass
from components.ui_elements.button.config import ButtonConfig

@dataclass
class SeriesConfig:
    series_name: str
    buttons: list[ButtonConfig]
    spacing: str = "gap-4"
    layout: str = "column"
    completion_icon: str = "done_all"
    log_severity: str = "positive"  # Align with NiceGUI's notification types: positive, warning, negative, info
    enable_run_all: bool = True
    run_all_label: str = "Run All Tasks"
    run_all_severity: str = "primary"
    run_all_icon: str = "play_arrow"
    run_all_completion_icon: str = "check_circle"
    progress_color: str = "primary"
    status_type: str = "ongoing"
    status_icon: str = "rotate_right"
