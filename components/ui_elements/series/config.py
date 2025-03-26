from pydantic import BaseModel, Field
from components.ui_elements.button.config import ButtonConfig

class SeriesConfig(BaseModel):
    """Configuration model for task series"""
    series_name: str
    buttons: list[ButtonConfig]
    spacing: str = Field("gap-4", description="CSS gap spacing between elements")
    layout: str = Field("column", description="Flex container layout direction")
    completion_icon: str = Field("done_all", description="Icon shown when series completes")
    log_severity: str = Field("positive", description="Default severity level for logs")
    enable_run_all: bool = Field(True, description="Show master run button")
    run_all_label: str = Field("Run All Tasks", description="Master button text")
    run_all_severity: str = Field("primary", description="Master button color severity")
    run_all_icon: str = Field("play_arrow", description="Master button icon")
    run_all_completion_icon: str = Field("check_circle", description="Completion icon for master button")
    progress_color: str = Field("primary", description="Progress bar color")
    status_type: str = Field("ongoing", description="Initial status label text")
    status_icon: str = Field("rotate_right", description="Status indicator icon")
    notification_duration: float = Field(3.0, description="How long notifications stay visible (seconds)")
