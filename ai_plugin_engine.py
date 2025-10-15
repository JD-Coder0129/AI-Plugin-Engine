from datetime import datetime
import time
import json
import os

PLUGIN_JSON_PATH = "plugins.json"

def load_plugins_from_json():
    if not os.path.exists(PLUGIN_JSON_PATH):
        return []
    with open(PLUGIN_JSON_PATH, "r") as f:
        data = json.load(f)
        return [JarvisPlugin(**plugin, from_json=True) for plugin in data]

def save_plugins_to_json():
    with open(PLUGIN_JSON_PATH, "w") as f:
        json.dump([plugin.to_dict() for plugin in JarvisPlugin.installed_plugins], f, indent=2)

class JarvisPlugin:
    """Represents a single AI plugin for Jarvis with metadata and utility methods."""

    installed_plugins = []

    def __init__(self, name, version, memory_usage, install_time=None, from_json=False):
        if not from_json and not JarvisPlugin.validate_plugin_data(name, version, memory_usage):
            raise ValueError("Invalid plugin data! Name must be string, version as str/float, memory positive integer.")

        self.name = name
        self.version = version
        self.memory_usage = memory_usage
        self.install_time = install_time or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if not from_json:
            JarvisPlugin.installed_plugins.append(self)
            save_plugins_to_json()
            print(f"✅ Plugin installed: {self.name} (v{self.version}) - {self.memory_usage}MB")

    def to_dict(self):
        return {
            "name": self.name,
            "version": self.version,
            "memory_usage": self.memory_usage,
            "install_time": self.install_time
        }

    # ---------- Magic Methods ----------
    def __str__(self):
        return f"🔹 Plugin: {self.name} (v{self.version}) - {self.memory_usage}MB"

    def __repr__(self):
        return f"JarvisPlugin(name={self.name!r}, version={self.version!r}, memory_usage={self.memory_usage!r})"

    def __len__(self):
        return self.memory_usage

    def __add__(self, other):
        if isinstance(other, JarvisPlugin):
            return self.memory_usage + other.memory_usage
        return NotImplemented

    def __eq__(self, other):
        if isinstance(other, JarvisPlugin):
            return (self.name, self.version) == (other.name, other.version)
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, JarvisPlugin):
            return self.memory_usage < other.memory_usage
        return NotImplemented

    # ---------- Static & Class Methods ----------
    @staticmethod
    def validate_plugin_data(name, version, memory_usage):
        return isinstance(name, str) and isinstance(version, (str, float)) and isinstance(memory_usage, int) and memory_usage > 0

    @classmethod
    def total_plugins(cls):
        return len(cls.installed_plugins)

    @classmethod
    def total_memory(cls):
        return sum(plugin.memory_usage for plugin in cls.installed_plugins)

    @classmethod
    def show_all_plugins(cls):
        if not cls.installed_plugins:
            return "No plugins currently installed."
        return "\n".join([str(p) for p in cls.installed_plugins])

class JarvisPluginManager:
    """Manages all plugin operations for Jarvis."""

    def __init__(self):
        self.plugins = []

    def add_plugin(self, plugin):
        if not isinstance(plugin, JarvisPlugin):
            print("❌ Invalid plugin type.")
            return
        if plugin in self.plugins:
            print(f"⚠️ Plugin {plugin.name} already added.")
        else:
            self.plugins.append(plugin)
            print(f"🔧 Plugin '{plugin.name}' successfully registered in Jarvis Manager.")

    def remove_plugin(self, plugin_name):
        for plugin in self.plugins:
            if plugin.name == plugin_name:
                self.plugins.remove(plugin)
                JarvisPlugin.installed_plugins.remove(plugin)
                save_plugins_to_json()
                print(f"🗑️ Plugin '{plugin_name}' uninstalled successfully.")
                return
        print(f"⚠️ Plugin '{plugin_name}' not found.")

    def list_plugins(self):
        if not self.plugins:
            return "No plugins installed in manager."
        return "\n".join(f"{idx+1}. {plugin}" for idx, plugin in enumerate(self.plugins))

    def show_all_plugins(self):
        return JarvisPlugin.show_all_plugins()

    def __len__(self):
        return len(self.plugins)

    def __str__(self):
        return f"Jarvis Plugin Manager: {len(self.plugins)} plugins loaded, {JarvisPlugin.total_memory()}MB total memory."

# ---------- Usage Example ----------
if __name__ == "__main__":
    print("=== ⚙️ Jarvis Plugin Engine v1 ===\n")

    # Load plugins from JSON file
    JarvisPlugin.installed_plugins = load_plugins_from_json()

    manager = JarvisPluginManager()
    # Add already installed plugins to manager
    for plugin in JarvisPlugin.installed_plugins:
        manager.add_plugin(plugin)

    # Create Plugins
    plugin1 = JarvisPlugin("Voice Assistant", "1.0", 120)
    plugin2 = JarvisPlugin("Reminder Manager", "2.1", 80)
    plugin3 = JarvisPlugin("Weather Analyzer", "1.5", 60)

    # Add to Manager
    print("\n🔧 Adding Plugins:")
    time.sleep(1)
    manager.add_plugin(plugin1)
    manager.add_plugin(plugin2)
    manager.add_plugin(plugin3)

    print("\n📜 Listing Installed Plugins:")
    time.sleep(1)
    print(manager.list_plugins())

    print("\n📊 System Summary:")
    time.sleep(1)
    print(manager)
    print(f"Total Plugins: {JarvisPlugin.total_plugins()}")
    print(f"Total Memory: {JarvisPlugin.total_memory()}MB")

    print("\n🧮 Plugin Comparison:")
    time.sleep(1)
    print(f"{plugin1.name} + {plugin2.name} = {plugin1 + plugin2}MB total memory")
    print(f"{plugin1.name} < {plugin2.name} ? {plugin1 < plugin2}")

    print("\n🗑️ Removing a Plugin:")
    time.sleep(1)
    manager.remove_plugin("Weather Analyzer")
    print(manager)

    print("\n📜 Showing All Plugins:")
    time.sleep(1)
    print(JarvisPlugin.show_all_plugins())