import asyncio
import traceback
import time

from components.ui_elements.base.config import SeverityLevel
from .config import SeriesConfig
from components.ui_elements.button.builder import ButtonBuilder
from nicegui import run, ui

class SeriesBuilder:
    """Constructs and manages a series of related UI tasks"""
    
    def __init__(self, config: SeriesConfig):
        self.config = config
        self.buttons = []

    def _notify(self, message: str, severity: str = 'info', log: bool = False):
        """Centralized notification handler with logging support"""
        if log:
            print(f"[{severity.upper()}] {message}")
        else:
            ui.notify(
                message,
                type=severity,
                icon=self.config.status_icon,
                timeout=self.config.notification_duration,
                close_button='Close'
            )
        
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
                    pass
        return self.container

    def delete(self):
        """Clean up all series components"""
        for btn in self.buttons:
            btn.delete()
        self.container.delete()

    def add_run_all_button(self):
        """Add master run button to top of series"""
        with self.container: 
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
        
        self._notify(
            f"Starting series '{self.config.series_name}'...",
            severity=self.config.status_type
        )

        for idx, btn in enumerate(self.buttons):
            task_num = idx + 1
            self.progress.value = idx / total_tasks
            self.status_label.set_text(f"{idx}/{total_tasks} tasks completed")
            btn.btn.loading = True
            ui.notify(f"Processing task {task_num}/{total_tasks}", type=self.config.status_type, timeout=2)
            try:
                btn.btn.props(f'icon={btn.config.default_icon} color={btn.config.severity}')
                await run.cpu_bound(ButtonBuilder._simulate_failure, task_num)
                success_count += 1
            except Exception as e:
                failure_count += 1
                failed_tasks.append((task_num, str(e)))
                btn.config.severity = SeverityLevel.ERROR
                btn.btn.props(f'color={btn.config.severity} icon=error')
                error_msg = f"Task {task_num} failed - see logs for details"
                self._notify(error_msg, severity='negative')
                self._notify(f"Task {task_num} error: {str(e)}\n{traceback.format_exc()}", severity='negative', log=True)
            
            completed = idx + 1
            self.progress.value = completed / total_tasks
            self.status_label.set_text(f"{completed}/{total_tasks} tasks completed")
            btn.btn.loading = False

        final_icon = self.config.run_all_completion_icon if failure_count == 0 else 'error'
        final_color = 'positive' if failure_count == 0 else 'negative'
        run_all_btn.props(f'icon={final_icon} color={final_color}')
        run_all_btn.loading = False

        if failed_tasks:
            self._notify(f"Completed with {failure_count} errors", severity='negative', log=True)
        else:
            self._notify(f"All {success_count} tasks completed successfully!", severity='positive')

        self.log_completion()

    def log_completion(self):
        """Log series completion with proper state handling"""
        self._notify(
            f"Completed series '{self.config.series_name}'",
            severity=self.config.log_severity,
            log=True
        )
