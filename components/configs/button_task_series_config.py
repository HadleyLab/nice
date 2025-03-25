from pydantic import BaseModel, Field

class ButtonTaskSeriesConfig(BaseModel):
    """Configuration model for a series of button tasks"""
    series_name: str = Field(..., description="Unique identifier for the task series")
    tasks: list[str] = Field(..., description="Ordered list of task names to execute")
    completion_delay: float = Field(1.0, description="Seconds between task completions")
    abort_on_failure: bool = Field(True, description="Stop series if any task fails")
    timeout: float = Field(5.0, description="Maximum execution time in seconds")
    button_label: str = Field("Run Series", description="Text displayed on the series trigger button")
    success_label: str = Field("Series Completed!", description="Text shown on successful completion")
    error_label: str = Field("Series Failed!", description="Text shown on series failure")
    button_color: str = Field("primary", description="NiceGUI color name for series button state")
    notification_duration: float = Field(5.0, description="Seconds to display final notifications")
    show_progress: bool = Field(True, description="Display progress bar during series execution")
