# Technology Stack

## Core Dependencies
- NiceGUI 1.4.1 (Reactive UI framework)
- Python 3.11 (Type hints, async/await)

## Key Patterns
- **State Management**: Native `ui.state()` for reactive properties
- **Component Architecture**: Prefer direct NiceGUI components over custom builders
- **Validation**: Leverage built-in validation and notifications
- **Async Operations**: Use NiceGUI's native async support

## Implementation Principles
1. Always prefer native NiceGUI functionality over custom implementations
2. Minimize custom builder patterns when standard components suffice
3. Utilize built-in state management and reactivity
4. Leverage NiceGUI's automatic DOM updates

## Critical Update
- Removed deprecated `ui.ref()` usage in favor of `ui.state()`
- Simplified reactive state management patterns
