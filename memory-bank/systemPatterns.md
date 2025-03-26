# System Architecture Patterns

## Reactive State Management
```mermaid
flowchart TD
    A[UI Element] --> B[ui.state()]
    B --> C[Automatic Binding]
    C --> D[DOM Update]
    D -->|User Interaction| A
```

### Implementation Patterns
1. **State Initialization**
   ```python
   # Dictionary-based state
   self.progress_state = ui.state({'value': 0.0})
   ```

2. **Reactive Binding**
   ```python
   ui.linear_progress().bind_value_from(self.progress_state, 'value')
   ```

3. **State Updates**
   ```python
   _, set_progress = ui.state({'value': 0.0})  # Tuple unpacking
   set_progress({'value': new_value})  # Proper state update
   ```

## Error Resolution History
- Fixed AttributeError: module 'nicegui.ui' has no attribute 'ref'
  - Migrated from deprecated `ui.ref()` to `ui.state()`
  - Updated all binding references to use dictionary access
  - Simplified state management pattern

## Current Best Practices
- Always use `ui.state()` with dictionary values
- Prefer `bind_value_from()` for reactive bindings
- Avoid tuple-state patterns
