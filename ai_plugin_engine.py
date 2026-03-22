from datetime import datetime
import time
import json
import os

# Try to import colorama for cross-platform colors; fallback to plain/no-op if unavailable
try:
    import colorama
    from colorama import Fore, Style
    colorama.init(autoreset=True)
except Exception:
    class _F:
        RED = '\033[31m'
        GREEN = '\033[32m'
        YELLOW = '\033[33m'
        BLUE = '\033[34m'
        MAGENTA = '\033[35m'
        CYAN = '\033[36m'
        RESET = '\033[0m'
    class _S:
        BRIGHT = '\033[1m'
        RESET_ALL = '\033[0m'
    Fore = _F()
    Style = _S()

C_RESET = Style.RESET_ALL
C_BOLD = Style.BRIGHT
C_GREEN = Fore.GREEN
C_RED = Fore.RED
C_YELLOW = Fore.YELLOW
C_BLUE = Fore.BLUE
C_CYAN = Fore.CYAN
C_MAGENTA = Fore.MAGENTA

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
    installed_plugins = []

    def __init__(self, name, version, memory_usage, install_time=None, from_json=False):
        if not from_json and not JarvisPlugin.validate_plugin_data(name, version, memory_usage):
            print(f"{C_RED}❌ Invalid plugin data!{C_RESET}")
            raise ValueError("Invalid plugin data! Name must be string, version as str/float, memory positive integer.")

        self.name = name
        self.version = version
        self.memory_usage = memory_usage
        self.install_time = install_time or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if not from_json:
            JarvisPlugin.installed_plugins.append(self)
            save_plugins_to_json()
            print(f"{C_GREEN}✅ Plugin installed: {C_BOLD}{self.name}{C_RESET}{C_GREEN} (v{self.version}) - {self.memory_usage}MB{C_RESET}")

    def to_dict(self):
        return {
            "name": self.name,
            "version": self.version,
            "memory_usage": self.memory_usage,
            "install_time": self.install_time
        }

    def __str__(self):
        return f"{C_CYAN}🔹 {C_BOLD}{self.name}{C_RESET}{C_CYAN} (v{self.version}){C_RESET}{C_MAGENTA} - {self.memory_usage}MB{C_RESET}"

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
            return f"{C_YELLOW}No plugins currently installed.{C_RESET}"
        lines = []
        for p in cls.installed_plugins:
            lines.append(str(p) + f" {C_BLUE}@ installed: {p.install_time}{C_RESET}")
        return "\n".join(lines)

class JarvisPluginManager:
    def __init__(self):
        self.plugins = []

    def add_plugin(self, plugin):
        if not isinstance(plugin, JarvisPlugin):
            print(f"{C_RED}❌ Invalid plugin type.{C_RESET}")
            return
        if plugin in self.plugins:
            print(f"{C_YELLOW}⚠️ Plugin {C_BOLD}{plugin.name}{C_RESET}{C_YELLOW} already added.{C_RESET}")
        else:
            self.plugins.append(plugin)
            print(f"{C_GREEN}🔧 Plugin '{C_BOLD}{plugin.name}{C_RESET}{C_GREEN}' successfully registered in Jarvis Manager.{C_RESET}")

    def remove_plugin(self, plugin_name):
        for plugin in self.plugins:
            if plugin.name == plugin_name:
                self.plugins.remove(plugin)
                try:
                    JarvisPlugin.installed_plugins.remove(plugin)
                except ValueError:
                    pass
                save_plugins_to_json()
                print(f"{C_GREEN}🗑️ Plugin '{C_BOLD}{plugin_name}{C_RESET}{C_GREEN}' uninstalled successfully.{C_RESET}")
                return
        print(f"{C_YELLOW}⚠️ Plugin '{C_BOLD}{plugin_name}{C_RESET}{C_YELLOW}' not found.{C_RESET}")

    def list_plugins(self):
        if not self.plugins:
            return f"{C_YELLOW}No plugins installed in manager.{C_RESET}"
        return "\n".join(f"{C_BLUE}{idx+1}. {C_RESET}{plugin}" for idx, plugin in enumerate(self.plugins))

    def show_all_plugins(self):
        return JarvisPlugin.show_all_plugins()

    def __len__(self):
        return len(self.plugins)

    def __str__(self):
        return (f"{C_MAGENTA}Jarvis Plugin Manager:{C_RESET} {C_BOLD}{len(self.plugins)}{C_RESET} plugins loaded, "
                f"{C_GREEN}{JarvisPlugin.total_memory()}MB{C_RESET} total memory.")

if __name__ == "__main__":
    print(f"{C_CYAN}{C_BOLD}=== ⚙️ Jarvis Plugin Engine v1 ==={C_RESET}\n")

    JarvisPlugin.installed_plugins = load_plugins_from_json()

    manager = JarvisPluginManager()
    for plugin in JarvisPlugin.installed_plugins:
        manager.add_plugin(plugin)

    # Sample installs (will print colored messages)
    plugin1 = JarvisPlugin("Voice Assistant", "1.0", 120)
    plugin2 = JarvisPlugin("Reminder Manager", "2.1", 80)
    plugin3 = JarvisPlugin("Weather Analyzer", "1.5", 60)

    print(f"\n{C_BLUE}🔧 Adding Plugins:{C_RESET}")
    time.sleep(0.5)
    manager.add_plugin(plugin1)
    manager.add_plugin(plugin2)
    manager.add_plugin(plugin3)

    print(f"\n{C_YELLOW}📜 Listing Installed Plugins:{C_RESET}")
    time.sleep(0.5)
    print(manager.list_plugins())

    print(f"\n{C_MAGENTA}📊 System Summary:{C_RESET}")
    time.sleep(0.5)
    print(manager)
    print(f"{C_BLUE}Total Plugins:{C_RESET} {C_BOLD}{JarvisPlugin.total_plugins()}{C_RESET}")
    print(f"{C_BLUE}Total Memory:{C_RESET} {C_GREEN}{JarvisPlugin.total_memory()}MB{C_RESET}")

    print(f"\n{C_CYAN}🧮 Plugin Comparison:{C_RESET}")
    time.sleep(0.5)
    print(f"{C_BOLD}{plugin1.name}{C_RESET} + {C_BOLD}{plugin2.name}{C_RESET} = {C_GREEN}{plugin1 + plugin2}MB{C_RESET} total memory")
    print(f"{C_BOLD}{plugin1.name}{C_RESET} < {C_BOLD}{plugin2.name}{C_RESET} ? {C_YELLOW}{plugin1 < plugin2}{C_RESET}")

    # print(f"\n{C_RED}🗑️ Removing a Plugin:{C_RESET}")
    # time.sleep(0.5)
    # manager.remove_plugin("Weather Analyzer")
    # print(manager)

    print(f"\n{C_YELLOW}📜 Showing All Plugins:{C_RESET}")
    time.sleep(0.5)
    print(JarvisPlugin.show_all_plugins())