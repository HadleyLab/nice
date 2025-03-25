# Architectural Patterns
1. Component Structure:
   - builders/: UI construction classes
     - 1:1 relationship with configs
     - Handles visual state/animations
   - configs/: State configuration objects
     - Color schemes
     - Icon mappings
     - Notification settings
   - utils/: Shared utilities
     - Centralized logging
     - Notification system

2. State Management:
   - Config objects drive builder behavior
   - Builders access config.* properties
   - State persisted in app.state.tasks

3. Animation Pattern:
   - CSS classes added/removed during state changes
   - Spin animation during active tasks
   - Config-driven transition durations
