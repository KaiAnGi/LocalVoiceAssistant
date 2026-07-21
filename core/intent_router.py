"""Intent routing - matches text to plugin actions via keywords."""


class IntentRouter:
    """Routes recognized text to plugin handlers based on keyword patterns."""

    def __init__(self):
        self._intents = []  # (pattern, plugin_name, action, module)

    def register_intent(self, pattern: str, plugin_name: str, action: str, plugin_module):
        self._intents.append((pattern, plugin_name, action, plugin_module))

    def route(self, text: str, bus) -> bool:
        """Match text against registered patterns, call handler. Returns True if handled."""
        text_lower = text.lower()
        matches = []

        for pattern, plugin_name, action, module in self._intents:
            if pattern.lower() in text_lower:
                matches.append((pattern, plugin_name, action, module))

        if not matches:
            return False

        # Longest pattern wins to resolve conflicts
        matches.sort(key=lambda m: len(m[0]), reverse=True)
        _, plugin_name, action, module = matches[0]

        print(f"[ROUTER] {plugin_name}.{action} <- '{matches[0][0]}'")

        if hasattr(module, "handle"):
            module.handle(action, text, bus)
            return True

        return False
