# Technical Stack
- NiceGUI for UI components
- Asyncio for async task handling
- Pydantic for data validation

## Component Structure
- `/components/ui_elements`
  - `/base` - Core UI element functionality
  - `/button` - Button implementations
  - `/series` - Series component implementations

## Validation Patterns
- Required field validation through `Field(min_length=1)`
- Post-model validation with `@model_validator`
- Unified validation for interdependent fields
- Strict type enforcement with `ConfigDict(extra="forbid")`

## State Management
- Config objects serialize to JSON
- Persisted in app.state.tasks
- Atomic state updates through _update_state()

## Notification System
- Native NiceGUI notifications with type-based styling
- Configurable icons and durations
- Automatic success/failure state tracking
- Channel-based routing (tasks/system)
