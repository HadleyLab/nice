from pydantic import BaseModel, Field

class ButtonTaskConfig(BaseModel):
    """Configuration model for a single button-driven async task"""
    task_name: str = Field(..., description="Unique identifier for the task")
    button_label: str = Field("Process Data", description="Text displayed on the button")
    success_label: str = Field("Data processed!", description="Text shown on success")
    error_label: str = Field("Processing failed", description="Text shown on failure")
    
    # State configuration
    initial_color: str = Field("blue", description="Initial state color")
    active_color: str = Field("teal", description="Active/running state color") 
    success_color: str = Field("green", description="Success state color")
    error_color: str = Field("red", description="Error state color")
    
    initial_icon: str = Field("more_horiz", description="Icon for initial state")
    active_icon: str = Field("autorenew", description="Spinner icon for active state")
    success_icon: str = Field("check", description="Icon for success state") 
    error_icon: str = Field("warning", description="Icon for error state")

    # Timing parameters
    timeout: float = Field(3.5, description="Maximum execution time in seconds")
    notification_duration: float = Field(4.0, description="Seconds to display notifications")
