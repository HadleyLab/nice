import asyncio

from components.ui_elements.base.config import SeverityLevel
from .config import SeriesConfig
from components.ui_elements.button.builder import ButtonBuilder
from nicegui import ui

class SeriesBuilder:
    """Constructs and manages a series of related UI tasks"""
    
    def __init__(self, config: SeriesConfig):
        self.config = config
        self.buttons = []
        
    def build(self):
        """Context manager for building the series"""
        self.container = ui.column().classes(f"{self.config.spacing} {self.config.layout}")
        with self.container:
            ui.label(self.config.series_name).classes("text-xl font-bold")
            self.progress = ui.linear_progress(0).props('instant-feedback').classes('w-full mb-2')
            self.status_label = ui.label().classes('text-sm mb-4')
            if self.config.enable_run_all:
                self.add_run_all_button()
            for btn_config in self.config.buttons:
                button = ButtonBuilder(btn_config)
                self.buttons.append(button)
                with button.build():
                    pass  # Button context handles its own rendering
        return self.container


    def delete(self):
        """Clean up all series components"""
        for btn in self.buttons:
            btn.delete()
        self.container.delete()

    def add_run_all_button(self):
        """Add master run button to top of series"""
        with self.container: 
            type_map = {
                'info': 'info',
                'success': 'positive',
                'warning': 'warning',
                'error': 'negative'
            }
            (ui.button(self.config.run_all_label, icon=self.config.run_all_icon)
                .props(f"unelevated color={self.config.run_all_severity} loading-spinner")
                .classes("w-full mb-4 p-4 font-bold rounded-lg hover:opacity-90 transition-all")
                .style("box-shadow: 0 2px 4px rgba(0,0,0,0.1);")
                .on_click(self.run_all))

    async def run_all(self, _=None):
        """Execute all tasks with proper state management and error handling"""
        run_all_btn = self.container.default_slot.children[1]
        run_all_btn.props(f'icon={self.config.run_all_icon} color={self.config.run_all_severity}')
        run_all_btn.loading = True
        success_count = 0
        failure_count = 0
        failed_tasks = []

        total_tasks = len(self.buttons)
        self.progress.value = 0
        self.status_label.set_text(f"0/{total_tasks} tasks completed")
        
        ui.notify(
            f"Starting series '{self.config.series_name}'...",
            type=self.config.status_type,
            icon=self.config.status_icon
        )

        for idx, btn in enumerate(self.buttons):
            task_num = idx + 1
            # Update progress and button state
            self.progress.value = idx / total_tasks
            self.status_label.set_text(f"{idx}/{total_tasks} tasks completed")
            btn.btn.loading = True
            ui.notify(f"Processing task {task_num}/{total_tasks}", type=self.config.status_type, timeout=2)
            try:
                # Reset button state before execution
                btn.btn.props(f'icon={btn.config.default_icon} color={btn.config.severity}')
                
                # Execute task with proper ID and wait for completion
                await asyncio.run.cpu_bound(
                    ButtonBuilder._simulate_failure,
                    task_num  # Pass the actual task number
                )
                success_count += 1

            except Exception as e:
                failure_count += 1
                failed_tasks.append((task_num, str(e)))
                btn.config.severity = SeverityLevel.ERROR
                btn.btn.props(f'color={btn.config.severity} icon=error')
                ui.notify(f"Task {idx+1} failed: {str(e)}", type='negative', timeout=3000)
            # Update progress after each task regardless of success
            completed = idx + 1
            self.progress.value = completed / total_tasks
            self.status_label.set_text(f"{completed}/{total_tasks} tasks completed")
            btn.btn.loading = False

        # Update Run All button state
        final_icon = self.config.run_all_completion_icon if failure_count == 0 else 'error'
        final_color = 'positive' if failure_count == 0 else 'negative'
        run_all_btn.props(f'icon={final_icon} color={final_color}')
        run_all_btn.loading = False

        # Show summary notification
        if failed_tasks:
            error_list = '\n'.join([f"Task {num}: {msg}" for num, msg in failed_tasks])
            ui.notify(f"Completed with {failure_count} errors:\n{error_list}", 
                     type='negative',
                     timeout=5000,
                     multi_line=True,
                     close_button='Close')
        else:
            ui.notify(f"All {success_count} tasks completed successfully!", 
                     type='positive',
                     icon=self.config.run_all_completion_icon)

        self.log_completion()

    def log_completion(self):
        """Log series completion with proper state handling"""
        notification_type = self.config.log_severity  # Directly use string value aligned with NiceGUI types
        
        ui.notify(
            f"Completed series '{self.config.series_name}'",
            type=notification_type,
            icon=self.config.completion_icon,
            timeout=self.config.buttons[0].notification_duration if self.config.buttons else 2000,
            clearable=True
        )
