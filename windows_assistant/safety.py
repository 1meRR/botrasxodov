from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class SafetyResult:
    required: bool
    reason: str = ""


class SafetyGuard:
    """Checks whether an operation requires explicit user confirmation."""

    def __init__(self, dangerous_keywords: tuple[str, ...]) -> None:
        self._keywords = tuple(word.lower() for word in dangerous_keywords)

    def requires_confirmation(self, command: str) -> SafetyResult:
        lower = command.lower()
        for keyword in self._keywords:
            if keyword in lower:
                return SafetyResult(required=True, reason=f"Обнаружен опасный шаблон: '{keyword}'.")
        return SafetyResult(required=False)
