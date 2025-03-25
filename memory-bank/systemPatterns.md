# System Architecture

```mermaid
flowchart TD
    UI[UI Layer] --> |Native Color Props| ButtonBuilder
    ButtonBuilder --> |Async Task| Core[Task Core]
    Core --> |Notifications| UI
    Config --> |Pydantic Model| ButtonBuilder
    Config --> |YAML| Persistence

    subgraph UI Layer
        ButtonBuilder
        LivePreview
        ConfigControls
    end

    subgraph Config
        ButtonTaskConfig
        defaults.yaml
    end
