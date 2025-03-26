# Architectural Patterns

## Component Relationships
```mermaid
flowchart TD
    BaseConfig --> ButtonConfig
    BaseConfig --> SeriesConfig
    ButtonConfig --> ButtonBuilder
    SeriesConfig --> SeriesBuilder
    Utils --> NotificationHandler
    Utils --> StateManager
    NotificationHandler --> ButtonBuilder
    StateManager --> ButtonBuilder
```

## Validation Workflow
```mermaid
flowchart TD
    Init[Model Init] --> FieldCheck[Field-level Validation]
    FieldCheck --> ModelCheck[Model Validator]
    ModelCheck -->|Valid| StateUpdate[Update State]
    ModelCheck -->|Invalid| Error[Raise ValueError]
    Error --> Notify[Error Notification]
    StateUpdate --> Render[UI Re-render]
```

## Notification Integration
- Centralized task_log_and_notify() handler
- Color-coded status messages
- Dual logging (console + UI)
- Error channel separation
