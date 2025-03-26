# Architectural Patterns
1. Component Structure:
   - Builders handle UI construction and state transitions
   - Configs manage persistent state and styling rules
   - Notifications system handles unified logging/feedback

2. Button Component Flow:
```mermaid
flowchart TD
    Click[Button Click] --> Handler[Click Handler]
    Handler --> Try[Try Block]
    Try --> UpdateState[Update Active State]
    Try --> SimulateTask[2s Timer]
    SimulateTask --> Complete[Mark Completed]
    Complete --> UpdateState
    Handler --> Catch[Catch Block]
    Catch --> ErrorState[Set Error State]
    ErrorState --> Notify[Show Error Notification]
    
    UpdateState --> Styles[Apply CSS Classes]
    UpdateState --> Log[Task Logging]
```

3. Notification Integration:
   - Centralized task_log_and_notify() handler
   - Color-coded status messages
   - Dual logging (console + UI)
   - Error channel separation
