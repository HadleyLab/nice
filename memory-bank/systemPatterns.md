# System Architecture

```mermaid
flowchart TD
    UI[UI Layer] --> |Native Color Props| ButtonBuilder
    ButtonBuilder --> |Async Task| Core[Task Core]
    Core --> |Notifications| UI
    Config --> |Pydantic Model| ButtonBuilder
    Config --> |YAML| Persistence
    
    subgraph Component_Hierarchy[Component Hierarchy]
        ParentContainer --> TaskButtons
        ParentContainer --> SeriesController
        SeriesController --> ProgressBar
    end

    subgraph UI Layer
        ButtonBuilder
        LivePreview
        ConfigControls
    end

    subgraph Config
        ButtonTaskConfig
        defaults.yaml
    end

# Styling Principles
1. **Parent-Child Styling**: Container components define layout/spacing
2. **Atomic Components**: Builder elements remain unstyled by default
3. **Spacing System**: Combined gap/margin utilities with parent delegation
4. **Structural Widths**: Components use w-full for responsive behavior  
5. **State Management**: Color changes handled through native props
6. **Style Isolation**: No component-level margin/padding definitions
