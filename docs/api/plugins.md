# Module: plugins

## Overview

Plugin system framework for SpreadsheetDL extensibility. Provides a comprehensive plugin architecture allowing users to extend SpreadsheetDL functionality with custom plugins through a well-defined interface.

**New in v4.0.0:**

- FR-EXT-001: Plugin system framework
- PluginInterface: Abstract base class for all plugins
- PluginHook: Event-based hook system for callbacks
- PluginLoader: Discovery and loading of plugins from directories
- PluginManager: Lifecycle management (register, enable, disable, list)

## Key Classes

### PluginInterface

Abstract base class that all plugins must implement to be discoverable by the plugin system.

**Abstract Properties:**

- `name` (str): Plugin name (unique identifier, lowercase, no spaces)
- `version` (str): Plugin version (semantic versioning, e.g., "1.0.0")

**Properties:**

- `description` (str): Human-readable plugin description (default: "")
- `author` (str): Author name or organization (default: "")

**Abstract Methods:**

#### `initialize(config: dict[str, Any] | None = None) -> None`

Initialize the plugin. Called when the plugin is enabled. Should perform any setup operations needed by the plugin.

**Parameters:**

- `config` (dict[str, Any] | None): Plugin configuration dictionary

**Example:**

```python
from spreadsheet_dl.plugins import PluginInterface

class MyPlugin(PluginInterface):
    @property
    def name(self) -> str:
        return "my_plugin"

    @property
    def version(self) -> str:
        return "1.0.0"

    def initialize(self, config=None):
        self.config = config or {}
        print(f"Initializing {self.name} with config: {self.config}")
```

**Methods:**

#### `shutdown() -> None`

Cleanup when plugin is disabled/unloaded. Called when the plugin is disabled. Should perform cleanup operations and release resources.

**Example:**

```python
def shutdown(self):
    print(f"Shutting down {self.name}")
    # Clean up resources
```

### PluginHook

Plugin hook system for pre/post operation callbacks. Provides event-based hooks that plugins can register callbacks for. Supports multiple callbacks per event.

**Implements:** FR-EXT-001: Plugin hook system

**Attributes:**

- `_hooks` (dict[str, list[Callable]]): Dictionary mapping event names to callback lists

**Methods:**

#### `__init__() -> None`

Initialize the hook system.

#### `register(event: str, callback: Callable[..., Any]) -> None`

Register callback for event.

**Parameters:**

- `event` (str): Event name to listen for
- `callback` (Callable): Callable to invoke when event is triggered

**Example:**

```python
from spreadsheet_dl.plugins import PluginHook

hooks = PluginHook()

def on_render_complete(output_path):
    print(f"Render completed: {output_path}")

hooks.register("render_complete", on_render_complete)
```

#### `unregister(event: str, callback: Callable[..., Any]) -> None`

Unregister callback from event.

**Parameters:**

- `event` (str): Event name
- `callback` (Callable): Callback to remove

#### `trigger(event: str, *args, **kwargs) -> list[Any]`

Trigger all callbacks for an event. Calls all registered callbacks for the event in order of registration. If a callback raises an exception, it is caught and logged, but does not prevent other callbacks from running.

**Parameters:**

- `event` (str): Event name to trigger
- `*args`: Positional arguments to pass to callbacks
- `**kwargs`: Keyword arguments to pass to callbacks

**Returns:**

- `list[Any]`: List of return values from all callbacks

**Example:**

```python
# Trigger event with arguments
results = hooks.trigger("before_render", sheet_spec=spec, output_path=path)
```

### PluginLoader

Discovers and loads plugins from directories. Scans Python files in plugin directories and discovers classes that implement the PluginInterface.

**Implements:** FR-EXT-001: Plugin discovery and loading

**Static Methods:**

#### `discover_plugins(plugin_dir: Path) -> list[type[PluginInterface]]`

Discover all plugins in directory. Scans the directory for Python files (excluding files starting with underscore) and finds classes that implement PluginInterface.

**Parameters:**

- `plugin_dir` (Path): Directory to scan for plugins

**Returns:**

- `list[type[PluginInterface]]`: List of plugin classes found

**Example:**

```python
from pathlib import Path
from spreadsheet_dl.plugins import PluginLoader

plugin_dir = Path.home() / ".spreadsheet-dl" / "plugins"
plugins = PluginLoader.discover_plugins(plugin_dir)
print(f"Found {len(plugins)} plugins")
```

#### `load_plugin(plugin_class: type[PluginInterface], config: dict[str, Any] | None = None) -> PluginInterface`

Instantiate and initialize a plugin. Creates an instance of the plugin class and calls its initialize method.

**Parameters:**

- `plugin_class` (type[PluginInterface]): Plugin class to instantiate
- `config` (dict[str, Any] | None): Plugin configuration

**Returns:**

- `PluginInterface`: Initialized plugin instance

**Example:**

```python
# Load and initialize plugin
plugin = PluginLoader.load_plugin(
    MyPlugin,
    config={"api_key": "xyz123"}
)
```

### PluginManager

Manages plugin lifecycle (register, enable, disable, list). Central manager for plugin operations. Discovers plugins from configured directories, tracks enabled/disabled state, and provides access to the hook system.

**Implements:** FR-EXT-001: Plugin lifecycle management

**Attributes:**

- `_plugins` (dict[str, PluginInterface]): Dictionary of all discovered plugins
- `_enabled` (set[str]): Set of enabled plugin names
- `_hooks` (PluginHook): Plugin hook system instance
- `_plugin_dirs` (list[Path]): Directories to search for plugins

**Methods:**

#### `__init__(plugin_dirs: list[Path] | None = None) -> None`

Initialize the plugin manager.

**Parameters:**

- `plugin_dirs` (list[Path] | None): List of directories to search for plugins. If None, uses default directories:
  - `~/.spreadsheet-dl/plugins`
  - `./plugins`

**Example:**

```python
from pathlib import Path
from spreadsheet_dl.plugins import PluginManager

# Use default directories
manager = PluginManager()

# Use custom directories
manager = PluginManager(plugin_dirs=[
    Path("/usr/share/spreadsheet-dl/plugins"),
    Path.home() / "my_plugins"
])
```

#### `discover() -> None`

Discover all available plugins. Scans plugin directories and registers discovered plugins. Does not enable plugins automatically.

**Example:**

```python
manager = PluginManager()
manager.discover()
```

#### `enable(name: str, config: dict[str, Any] | None = None) -> None`

Enable a plugin. Initializes and enables a previously discovered plugin.

**Parameters:**

- `name` (str): Plugin name
- `config` (dict[str, Any] | None): Plugin configuration dictionary

**Raises:**

- `ValueError`: If plugin not found

**Example:**

```python
# Enable plugin with config
manager.enable("my_plugin", config={"key": "value"})
```

#### `disable(name: str) -> None`

Disable a plugin. Shuts down and disables an enabled plugin.

**Parameters:**

- `name` (str): Plugin name

**Example:**

```python
manager.disable("my_plugin")
```

#### `list_plugins(enabled_only: bool = False) -> list[dict[str, Any]]`

List all plugins with metadata.

**Parameters:**

- `enabled_only` (bool): If True, only return enabled plugins

**Returns:**

- `list[dict[str, Any]]`: List of plugin metadata dictionaries with keys:
  - `name` (str): Plugin name
  - `version` (str): Plugin version
  - `description` (str): Plugin description
  - `author` (str): Plugin author
  - `enabled` (bool): Whether plugin is enabled

**Example:**

```python
# List all plugins
all_plugins = manager.list_plugins()

# List only enabled plugins
enabled = manager.list_plugins(enabled_only=True)

for plugin in all_plugins:
    status = "enabled" if plugin["enabled"] else "disabled"
    print(f"{plugin['name']} v{plugin['version']} ({status})")
```

#### `get_plugin(name: str) -> PluginInterface | None`

Get plugin instance by name.

**Parameters:**

- `name` (str): Plugin name

**Returns:**

- `PluginInterface | None`: Plugin instance or None if not found

#### `hooks -> PluginHook`

Property that provides access to the hook system.

**Returns:**

- `PluginHook`: Plugin hook system instance

**Example:**

```python
manager = PluginManager()
manager.hooks.register("event", callback)
```

## Key Functions

### get_plugin_manager() -> PluginManager

Get or create global plugin manager. Provides singleton access to the plugin manager. Creates and discovers plugins on first call.

**Returns:**

- `PluginManager`: Global PluginManager instance

**Example:**

```python
from spreadsheet_dl.plugins import get_plugin_manager

manager = get_plugin_manager()
plugins = manager.list_plugins()
```

## Usage Examples

### Creating a Simple Plugin

```python
# File: ~/.spreadsheet-dl/plugins/hello_plugin.py
from spreadsheet_dl.plugins import PluginInterface

class HelloPlugin(PluginInterface):
    @property
    def name(self) -> str:
        return "hello"

    @property
    def version(self) -> str:
        return "1.0.0"

    @property
    def description(self) -> str:
        return "Simple hello world plugin"

    @property
    def author(self) -> str:
        return "John Doe"

    def initialize(self, config=None):
        print("Hello from plugin!")
        self.config = config or {}

    def shutdown(self):
        print("Goodbye from plugin!")
```

### Using the Plugin via CLI

```bash
# List all discovered plugins
spreadsheet-dl plugin list

# Enable the plugin
spreadsheet-dl plugin enable hello

# Disable the plugin
spreadsheet-dl plugin disable hello

# Show plugin info
spreadsheet-dl plugin info hello
```

### Creating a Plugin with Hooks

```python
# File: ~/.spreadsheet-dl/plugins/render_logger.py
from pathlib import Path
from spreadsheet_dl.plugins import PluginInterface, get_plugin_manager

class RenderLoggerPlugin(PluginInterface):
    @property
    def name(self) -> str:
        return "render_logger"

    @property
    def version(self) -> str:
        return "1.0.0"

    @property
    def description(self) -> str:
        return "Logs all render operations"

    def initialize(self, config=None):
        self.config = config or {}
        self.log_file = Path(self.config.get("log_file", "render.log"))

        # Register hooks
        manager = get_plugin_manager()
        manager.hooks.register("before_render", self.on_before_render)
        manager.hooks.register("after_render", self.on_after_render)

    def on_before_render(self, sheets, output_path):
        msg = f"Starting render: {output_path}, {len(sheets)} sheet(s)\n"
        self.log_file.write_text(msg, encoding="utf-8")

    def on_after_render(self, output_path):
        msg = f"Completed render: {output_path}\n"
        with self.log_file.open("a") as f:
            f.write(msg)

    def shutdown(self):
        print(f"Render logger saved to {self.log_file}")
```

### Programmatic Plugin Management

```python
from pathlib import Path
from spreadsheet_dl.plugins import PluginManager

# Create manager with custom directories
manager = PluginManager(plugin_dirs=[
    Path("/opt/spreadsheet-dl/plugins"),
    Path.home() / ".local/share/spreadsheet-dl/plugins"
])

# Discover plugins
manager.discover()

# List all plugins
plugins = manager.list_plugins()
for plugin in plugins:
    print(f"{plugin['name']}: {plugin['description']}")

# Enable plugin with configuration
manager.enable("my_plugin", config={
    "api_endpoint": "https://api.example.com",
    "timeout": 30
})

# Use hooks
manager.hooks.register("custom_event", lambda x: print(f"Event: {x}"))
manager.hooks.trigger("custom_event", "Hello")

# Disable plugin
manager.disable("my_plugin")
```

### Advanced Plugin with Multiple Hooks

```python
from spreadsheet_dl.plugins import PluginInterface, get_plugin_manager
from datetime import datetime

class AnalyticsPlugin(PluginInterface):
    @property
    def name(self) -> str:
        return "analytics"

    @property
    def version(self) -> str:
        return "1.0.0"

    @property
    def description(self) -> str:
        return "Tracks usage analytics"

    def initialize(self, config=None):
        self.config = config or {}
        self.stats = {
            "renders": 0,
            "exports": 0,
            "errors": 0,
        }

        manager = get_plugin_manager()
        manager.hooks.register("before_render", self.on_render)
        manager.hooks.register("before_export", self.on_export)
        manager.hooks.register("on_error", self.on_error)

    def on_render(self, *args, **kwargs):
        self.stats["renders"] += 1
        print(f"Render #{self.stats['renders']}")

    def on_export(self, *args, **kwargs):
        self.stats["exports"] += 1
        print(f"Export #{self.stats['exports']}")

    def on_error(self, error, *args, **kwargs):
        self.stats["errors"] += 1
        print(f"Error occurred: {error}")

    def shutdown(self):
        print("Analytics Summary:")
        print(f"  Renders: {self.stats['renders']}")
        print(f"  Exports: {self.stats['exports']}")
        print(f"  Errors: {self.stats['errors']}")
```

## Plugin Development Best Practices

### 1. Plugin Structure

```python
# Good plugin structure
class MyPlugin(PluginInterface):
    # Required properties
    @property
    def name(self) -> str:
        return "my_plugin"  # Use lowercase, no spaces

    @property
    def version(self) -> str:
        return "1.0.0"  # Semantic versioning

    # Optional but recommended
    @property
    def description(self) -> str:
        return "Clear description of functionality"

    @property
    def author(self) -> str:
        return "Your Name <email@example.com>"

    # Lifecycle methods
    def initialize(self, config=None):
        # Validate config
        # Set up resources
        # Register hooks
        pass

    def shutdown(self):
        # Clean up resources
        # Unregister hooks (if needed)
        # Save state
        pass
```

### 2. Error Handling

```python
def initialize(self, config=None):
    try:
        self.config = config or {}
        # Validate required config
        if "api_key" not in self.config:
            raise ValueError("api_key is required in config")

        # Initialize with error handling
        self.setup_resources()
    except Exception as e:
        print(f"Plugin initialization failed: {e}")
        raise

def setup_resources(self):
    # Resource setup with proper error handling
    pass
```

### 3. Hook Usage

```python
def initialize(self, config=None):
    manager = get_plugin_manager()

    # Register hooks with bound methods
    manager.hooks.register("event", self.handle_event)

def handle_event(self, *args, **kwargs):
    try:
        # Handle event safely
        pass
    except Exception as e:
        print(f"Hook error: {e}")
        # Don't re-raise - let other plugins continue
```

## See Also

- [cli](cli.md) - Plugin management commands
- [exceptions](exceptions.md) - Plugin-related exceptions (PluginNotFoundError, PluginLoadError, HookError)
- [config](config.md) - Plugin configuration
