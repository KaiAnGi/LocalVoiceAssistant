"""Plugin discovery and registration."""

import importlib.util
import json
from pathlib import Path


PLUGINS_DIR = Path(__file__).parent.parent / "plugins"


def load_plugins(bus, router):
    """Discover and load all plugins from plugins/ directory."""
    for plugin_dir in sorted(PLUGINS_DIR.iterdir()):
        if not plugin_dir.is_dir():
            continue

        manifest_path = plugin_dir / "manifest.json"
        plugin_path = plugin_dir / "plugin.py"

        if not manifest_path.exists() or not plugin_path.exists():
            continue

        try:
            with open(manifest_path, encoding="utf-8") as f:
                manifest = json.load(f)

            name = manifest["name"]

            spec = importlib.util.spec_from_file_location(name, plugin_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            if hasattr(module, "init"):
                module.init(bus)

            for intent in manifest.get("intents", []):
                router.register_intent(
                    pattern=intent["pattern"],
                    plugin_name=name,
                    action=intent["action"],
                    plugin_module=module,
                )

            print(f"[PLUGIN] Loaded: {name} v{manifest.get('version', '?')}")
        except Exception as e:
            print(f"[PLUGIN] Failed to load {plugin_dir.name}: {e}")
