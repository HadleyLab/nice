from nicegui import ui, run
from pydantic import BaseModel, Field
from typing import Optional, Any
import yaml
import asyncio
import time  # Added for synchronous sleep

# ---------- Models ----------
class ButtonTaskConfig(BaseModel):
    """Configuration model for a single button-driven async task"""
    task_name: str = Field(..., description="Unique identifier for the task")
    button_label: str = Field("Process Data", description="Text displayed on the button")
    success_label: str = Field("Data processed!", description="Text shown on success")
    error_label: str = Field("Processing failed", description="Text shown on failure")
    button_color: str = Field("primary", description="NiceGUI color name for button state")
    timeout: float = Field(3.5, description="Maximum execution time in seconds")
    notification_duration: float = Field(4.0, description="Seconds to display notifications")
    
class ButtonSeriesConfig(BaseModel):
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

# ---------- Builders ----------

class ButtonTaskBuilder:
    """Constructs and manages an async task with UI controls"""
    
    def __init__(self, config: ButtonTaskConfig):
        self.config = config
        self._create_ui()

    def delete(self):
        """Clean up all UI components"""
        self.container.delete()
        
    def _create_ui(self):
        """Build the UI components for this task"""
        self.container = ui.column()
        with self.container:
            self.btn = ui.button(self.config.task_name).props("color=primary")
            self.btn.on("click", self._execute_task)
            
            self.status = ui.label().classes("text-sm")
            self.progress = ui.linear_progress().classes("w-full")

    async def _execute_task(self):
        """Execute task with progress tracking"""
        try:
            self.btn.props("loading=spin")
            await asyncio.sleep(1.5)  # Simulated work
            self.progress.value = 1.0
            ui.notify(f"{self.config.task_name} completed", type='positive')
        except Exception as e:
            ui.notify(f"{self.config.task_name} failed: {str(e)}", type='negative')
        finally:
            self.btn.props("loading=false")

class ButtonTaskSeriesBuilder:
    """Coordinates execution of multiple ButtonTasks in sequence"""
    
    def __init__(self, config: ButtonSeriesConfig, task_builders: dict[str, ButtonTaskBuilder]):
        self.config = config
        self.task_builders = task_builders
        self._create_ui()
        
    def _create_ui(self):
        """Build series UI components"""
        self.container = ui.column()
        with self.container:
            with ui.button(self.config.button_label).props(f"color={self.config.button_color}") as self.btn:
                self.btn.on("click", self._execute_task)
            
            self.status_label = ui.label().classes("text-sm ml-2")
            self.notification = ui.notification(position="bottom-right")

    def delete(self):
        """Clean up all UI components"""
        self.notification.clear()
        self.container.delete()

    async def _execute_task(self):
        """Handle task execution with UI state management"""
        try:
            self._set_ui_state(running=True)
            result = await asyncio.wait_for(
                run.io_bound(self._mock_task), 
                timeout=self.config.timeout
            )
            self._show_result(success=True, message=f"{self.config.success_label}: {result}")
        except Exception as e:
            self._show_result(success=False, message=f"{self.config.error_label}: {str(e)}")
        finally:
            self._set_ui_state(running=False)

    def _set_ui_state(self, running: bool):
        """Update UI elements based on task state"""
        self.btn.props(f"loading={'spin' if running else ''}")
        self.status_label.set_text("Running..." if running else "")

    def _show_result(self, success: bool, message: str):
        """Display task outcome notification"""
        ui.notify(message, type='positive' if success else 'negative', timeout=self.config.notification_duration)

    def _mock_task(self):
        """Example task that simulates work"""
        time.sleep(1.5)
        return "Task completed successfully"

# ---------- Demo Setup ----------
def configure_demo():
    """Interactive demo with live configuration"""
    # Create stateful configuration
    class DemoState:
        def __init__(self):
            # Load default configuration from YAML
            with open('defaults.yaml') as f:
                yaml_data = yaml.safe_load(f)
            # Load and validate configuration
            if 'button_task' not in yaml_data or 'button_task_series' not in yaml_data:
                raise KeyError("Missing required configuration sections in defaults.yaml")
                
            self.task_config = ButtonTaskConfig(**yaml_data['button_task'])
            self.series_config = ButtonSeriesConfig(**yaml_data['button_task_series'])
            self.task_builders = {}
        
        @ui.refreshable
        def update_task_config(self, **kwargs):
            self.task_config = self.task_config.copy(update=kwargs)
            return self.task_config
            
        @ui.refreshable
        def update_series_config(self, **kwargs):
            self.series_config = self.series_config.copy(update=kwargs)
            return self.series_config

    state = DemoState()
    
    # Create initial task builders
    state.task_builders = {
        "task1": ButtonTaskBuilder(state.task_config),
        "task2": ButtonTaskBuilder(state.task_config)
    }
    
    # Store builder references for refresh
    task_builder_ref = None
    series_builder_ref = ButtonTaskSeriesBuilder(state.series_config, state.task_builders)
    
    with ui.column().classes("w-full max-w-2xl mx-auto p-4 gap-4"):
        ui.label("Interactive Configuration").classes("text-2xl mb-4")
        
        # Configuration Controls
        with ui.card().classes("w-full p-4 gap-2 border"):
            ui.label("Task Parameters").classes("text-lg font-bold")
            
            with ui.grid(columns=2).classes("w-full gap-4"):
                ui.input("Button Label", on_change=lambda e: state.update_task_config(button_label=e.value)
                    ).bind_value(state.task_config, "button_label")
                ui.input("Success Message", on_change=lambda e: state.update_task_config(success_label=e.value)
                    ).bind_value(state.task_config, "success_label")
                ui.input("Error Message", on_change=lambda e: state.update_task_config(error_label=e.value)
                    ).bind_value(state.task_config, "error_label")
                ui.number("Timeout (seconds)", min=0.1, max=60, step=0.1,
                         on_change=lambda e: state.update_task_config(timeout=e.value)
                         ).bind_value(state.task_config, "timeout")
                ui.number("Notification Duration", min=0.5, max=10, step=0.5,
                         on_change=lambda e: state.update_task_config(notification_duration=e.value)
                         ).bind_value(state.task_config, "notification_duration")
                ui.select(['primary', 'positive', 'negative', 'warning'], 
                         label="Button Color",
                         on_change=lambda e: state.update_task_config(button_color=e.value)
                         ).bind_value(state.task_config, "button_color")
                
            with ui.card().classes("w-full p-4 gap-2 border"):
                ui.label("Series Parameters").classes("text-lg font-bold")
                with ui.grid(columns=2).classes("w-full gap-4"):
                    ui.input("Series Name", on_change=lambda e: state.update_series_config(series_name=e.value)
                        ).bind_value(state.series_config, "series_name")
                    ui.number("Completion Delay", min=0.1, max=10, step=0.1,
                            on_change=lambda e: state.update_series_config(completion_delay=e.value)
                            ).bind_value(state.series_config, "completion_delay")
                    ui.number("Timeout", min=1, max=60, step=1,
                            on_change=lambda e: state.update_series_config(timeout=e.value)
                            ).bind_value(state.series_config, "timeout")
                    ui.checkbox("Abort on Failure", on_change=lambda e: state.update_series_config(abort_on_failure=e.value)
                        ).bind_value(state.series_config, "abort_on_failure")
        
        # Live Preview
        with ui.card().classes("w-full p-4 border"):
            ui.label("Live Preview").classes("text-lg font-bold mb-2")
            
            def refresh_preview():
                nonlocal series_builder_ref
                
                # Refresh task builders
                for builder in state.task_builders.values():
                    builder.delete()
                state.task_builders = {
                    "task1": ButtonTaskBuilder(state.task_config),
                    "task2": ButtonTaskBuilder(state.task_config)
                }
                
                # Refresh series builder
                series_builder_ref.delete()
                series_builder_ref = ButtonTaskSeriesBuilder(state.series_config, state.task_builders)
                
                # Clear notifications
                ui.notification(position="bottom-right").clear()
            
            with ui.column().classes("w-full items-center gap-4"):
                ui.button("Refresh All Components", on_click=refresh_preview)
                list(state.task_builders.values())[0].container
                list(state.task_builders.values())[1].container
                series_builder_ref.container
        
@ui.page('/')
def main_page():
    configure_demo()

if __name__ in {"__main__", "__mp_main__"}:
    ui.run(host='0.0.0.0', port=8080, show=False)
