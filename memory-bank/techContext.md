# Technical Stack
- NiceGUI for UI components
- Asyncio for async task handling
- Component Structure:
  - /components
    /builders - UI construction (1:1 with configs)
    /configs - State configurations (colors, icons, durations)
    /utils - Shared utilities (logging/notifications)
- State Management:
  - Config objects serialize to JSON
  - Persisted in app.state.tasks
  - Atomic state updates through _update_state()
- Notification System:
  - Native NiceGUI notifications with type-based styling
  - Configurable icons and durations
  - Automatic success/failure state tracking
  - Configurable display durations
  - Channel-based routing (tasks/system)
