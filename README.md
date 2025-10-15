# ⚙️ Jarvis Plugin Engine (v2)

> A modular AI plugin management system that allows **Jarvis** 🤖 to install, track, and persist its “skills” across sessions — now with **JSON storage**!  
> This system simulates how real AI assistants dynamically manage and remember their functional modules.

---

## 🧠 Overview

The **Jarvis Plugin Engine** manages individual AI modules such as:

- 🎙️ Voice Assistant  
- ⏰ Reminder Manager  
- 🌦️ Weather Analyzer  

Each module (plugin) has its own **name**, **version**, and **memory usage**, and is stored persistently in a **JSON file**, even after the program closes.  
This design demonstrates key OOP concepts:  
✔️ Static & Class Methods  
✔️ Magic Methods  
✔️ File Persistence (JSON)  
✔️ Encapsulation & Composition  

---

## 🧩 Features

- 🧱 **Dynamic Plugin Management** – Add, remove, and view installed plugins easily  
- 💾 **Persistent Storage (JSON)** – Saves all plugin data to `plugins.json` for future runs  
- 🧮 **Memory & Version Tracking** – Monitors plugin resource usage and compatibility  
- 🧠 **Static Validation** – Ensures plugins are valid before installation  
- 🧾 **System Summary** – Displays installed plugin count and total memory  
- 🔄 **Global Plugin Overview** – `show_all_plugins()` displays every installed plugin (even across sessions)  
- 🧰 **Magic Method Integration**  
  - `__add__` → Combine memory usage  
  - `__eq__` → Compare plugins  
  - `__lt__` → Sort plugins by memory usage  
  - `__len__` → Memory footprint  
  - `__str__`, `__repr__` → Clean readable outputs  

---

## 🧠 Class Architecture

```text
JarvisPluginManager
 └── Manages → JarvisPlugin (Instances)
         ├── Class Variable: installed_plugins
         ├── Static Method: validate_plugin_data()
         ├── Class Methods: total_plugins(), total_memory(), show_all_plugins(), load_from_json(), save_to_json()
         ├── Magic Methods: __str__, __repr__, __add__, __eq__, __lt__, __len__
         ├── JSON File: plugins.json (Persistent Storage)
