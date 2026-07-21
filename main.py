"""Jarvis Voice Assistant - Entry point."""

from core.event_bus import EventBus
from core.audio_input import SpeechRecognizer
from core.audio_output import Speaker
from core.intent_router import IntentRouter
from core.plugin_loader import load_plugins


def main():
    bus = EventBus()
    router = IntentRouter()

    speaker = Speaker()
    bus.subscribe("speak", lambda text: speaker.speak(text))

    load_plugins(bus, router)

    recognizer = SpeechRecognizer()

    print("Jarvis ready. Say something (Ctrl+C to quit).")
    try:
        while True:
            text = recognizer.listen_once()
            print(f"You: {text}")
            if not router.route(text, bus):
                print("(no matching command)")
    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        recognizer.cleanup()


if __name__ == "__main__":
    main()
