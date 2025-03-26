from nicegui import ui
from components.ui_elements.base.builder import BaseLayout

def create():
    """About page with application information"""
    with BaseLayout() as content:
        ui.label("About This App").classes('text-3xl font-bold mb-4')
        with ui.card().classes('w-full p-4'):
            ui.markdown('''
                ### Application Overview
                - Built with NiceGUI
                - Modular component architecture
                - Config-driven UI development
            ''')
