from dataclasses import dataclass
from components.ui_elements.button.config import ButtonConfig

@dataclass
class SeriesConfig:
    series_name: str
    buttons: list[ButtonConfig]
    spacing: str = "gap-4"
    layout: str = "column"
    completion_icon: str = "done_all"
    log_severity: str = "info"
