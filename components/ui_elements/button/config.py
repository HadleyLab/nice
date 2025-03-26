from pydantic import Field, model_validator, ConfigDict
from ..base.config import BaseConfig, SeverityLevel

class ButtonConfig(BaseConfig):
    """Configuration for interactive button elements"""
    uid: str = Field(min_length=1)
    task_name: str = Field(default="New Task", min_length=1)
    default_icon: str = Field(default="play_arrow", pattern=r"^[a-z_]+$")
    active_icon: str = Field(default="hourglass_empty", pattern=r"^[a-z_]+$")
    completion_icon: str = Field(default="check", pattern=r"^[a-z_]+$")
    notification_duration: int = Field(default=3000, gt=0)
    failure_rate: float = Field(default=0.2, ge=0, le=1)
    severity: SeverityLevel = Field(default=SeverityLevel.INFO)

    @model_validator(mode="after")
    def validate_required_fields(self) -> "ButtonConfig":
        if not self.uid:
            raise ValueError("UID is required")
        if not self.task_name:
            raise ValueError("Task name is required")
        return self

    model_config = ConfigDict(
        extra="forbid",
        validate_default=True
    )
