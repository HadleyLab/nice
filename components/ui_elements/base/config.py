from enum import StrEnum, Enum
from pydantic import BaseModel, ConfigDict, Field, model_validator
from pydantic_settings import BaseSettings

class SeverityLevel(str, Enum):
    """Standardized severity levels mapped to NiceGUI colors"""
    INFO = 'info'
    SUCCESS = 'positive'
    WARNING = 'warning'
    ERROR = 'negative'
    DEFAULT = 'primary'

class Color(StrEnum):
    """Mirror of NiceGUI's color palette with additional semantic meanings"""
    PRIMARY = 'primary'
    SECONDARY = 'secondary'
    ACCENT = 'accent'
    POSITIVE = 'positive'
    NEGATIVE = 'negative'
    WARNING = 'warning'
    INFO = 'info'
    DARK = 'dark'
    LIGHT = 'light'
    TRANSPARENT = 'transparent'
    
    # Semantic mappings
    SUCCESS = POSITIVE
    ERROR = NEGATIVE
    ALERT = 'warning'

class BaseConfig(BaseModel):
    """Base configuration model for UI elements"""
    label: str = Field(default="Button", min_length=1)
    color: Color = Field(default=Color.PRIMARY)
    state: str = Field(default="default", pattern=r"^(active|completed|error|default)$")
    default_notification_duration: float = Field(2.5, description="Default duration for notifications in seconds")
    
    model_config = ConfigDict(
        use_enum_values=True,
        validate_assignment=True,
        extra="forbid"
    )

    @classmethod
    def get_severity(cls, exception: Exception) -> SeverityLevel:
        """Map exception types to standardized severity levels"""
        if isinstance(exception, ValueError):
            return SeverityLevel.WARNING
        if isinstance(exception, TypeError):
            return SeverityLevel.ERROR
        return SeverityLevel.ERROR  # Default to ERROR

class AppSettings(BaseSettings):
    """Global application settings"""
    debug: bool = False
    strict_validation: bool = True
    animation_duration: int = Field(200, gt=0)
    
    model_config = ConfigDict(
        env_file=".env",
        env_prefix="NICEGUI_",
        extra="ignore"
    )

class SeverityLevel(str, Enum):
    """Standardized severity levels mapped to NiceGUI colors"""
    INFO = 'info'
    SUCCESS = 'positive'
    WARNING = 'warning'
    ERROR = 'negative'
    DEFAULT = 'primary'
