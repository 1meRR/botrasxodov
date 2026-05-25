from __future__ import annotations

from assistant import Assistant
from actions import ActionExecutor
from config import AssistantConfig
from nlp import CommandParser
from safety import SafetyGuard
from voice import VoiceEngine


def build_assistant() -> Assistant:
    config = AssistantConfig()
    config.ensure_dirs()

    voice = VoiceEngine(vosk_model_path=str(config.vosk_model_path), use_vosk_offline=config.use_vosk_offline)
    parser = CommandParser()
    actions = ActionExecutor(
        screenshots_dir=config.screenshots_dir,
        notes_dir=config.notes_dir,
        allow_terminal_commands=config.allow_terminal_commands,
    )
    safety = SafetyGuard(config.dangerous_keywords)

    return Assistant(voice=voice, parser=parser, actions=actions, safety=safety)


def run() -> None:
    app = build_assistant()
    app.voice.speak("Ассистент запущен. Скажите команду.")

    while True:
        try:
            heard = app.voice.listen_once(timeout=10, phrase_time_limit=10)
            if not heard:
                continue
            normalized = heard.lower().strip()

            if normalized in {"стоп", "выход", "заверши работу"}:
                app.voice.speak("Останавливаюсь. До свидания.")
                break

            response = app.handle(heard)
            app.voice.speak(response)
        except KeyboardInterrupt:
            app.voice.speak("Остановка по запросу пользователя.")
            break
        except Exception as exc:
            app.voice.speak(f"Ошибка: {exc}")


if __name__ == "__main__":
    run()
