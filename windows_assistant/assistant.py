from __future__ import annotations

from dataclasses import dataclass

from actions import ActionExecutor
from nlp import CommandParser
from safety import SafetyGuard
from voice import VoiceEngine


@dataclass(slots=True)
class Assistant:
    voice: VoiceEngine
    parser: CommandParser
    actions: ActionExecutor
    safety: SafetyGuard

    def handle(self, text: str) -> str:
        safety_result = self.safety.requires_confirmation(text)
        if safety_result.required:
            self.voice.speak(f"Нужно подтверждение. {safety_result.reason} Скажите: подтверждаю или отмена.")
            decision = self.voice.listen_once(timeout=6, phrase_time_limit=4) or ""
            if "подтверждаю" not in decision.lower():
                return "Операция отменена пользователем."

        parsed = self.parser.parse(text)
        intent = parsed.intent
        payload = parsed.payload

        if intent == "open_website":
            return self.actions.open_website(payload["url"])
        if intent == "open_app":
            return self.actions.open_app(payload["app"])
        if intent == "type_text":
            return self.actions.type_text(payload["text"])
        if intent == "press_keys":
            keys = tuple(k for k in payload["keys"].split(",") if k)
            return self.actions.press_keys(*keys)
        if intent == "move_mouse":
            return self.actions.move_mouse(int(payload["x"]), int(payload["y"]))
        if intent == "screenshot":
            return self.actions.screenshot()
        if intent == "create_note":
            return self.actions.create_note(payload["filename"], payload["content"])
        if intent == "search_file":
            return self.actions.search_file(payload["query"])
        if intent == "run_command":
            return self.actions.run_safe_command(payload["command"])
        if intent == "answer":
            return self.answer(payload["question"])

        return "Не понял команду. Повторите иначе."

    @staticmethod
    def answer(question: str) -> str:
        q = question.lower()
        if "время" in q:
            from datetime import datetime

            return f"Сейчас {datetime.now().strftime('%H:%M')}"
        if "дата" in q:
            from datetime import datetime

            return f"Сегодня {datetime.now().strftime('%d.%m.%Y')}"
        return (
            "Я локальный ассистент. Могу открывать приложения, печатать, делать скриншоты, "
            "искать файлы и выполнять безопасные команды."
        )
