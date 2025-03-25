# Technical Context

## Core Technologies
- NiceGUI 1.4+ (Native color system)
- Pydantic 2.5+ (Configuration validation)
- Python 3.10+ (Async/await syntax)
- YAML configuration loader

## Development Environment Setup
```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/MacOS
.\.venv\Scripts\activate   # Windows

# Install dependencies
pip install nicegui pydantic pyyaml
```

## Key Implementation Details
- Color system uses NiceGUI's built-in options (primary/positive/negative/warning)
- Configuration strictly matches Pydantic model fields
- Async task management with timeout handling
- Live preview system with reactive configuration

## Development Practices
- Memory Bank-driven documentation
- Configuration-first design pattern
- UI component isolation in Builder classes
- Strict type validation with Pydantic
- Virtual environment convention (see .clinerules)

## Troubleshooting
- Port conflicts: Use `ui.run(port=8081)` to change default port
- YAML validation: Ensure field names match Pydantic model exactly
