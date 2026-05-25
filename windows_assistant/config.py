from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable


DANGEROUS_KEYWORDS: tuple[str, ...] = (
    "удали",
    "удалить",
    "стереть",
    "отправь письмо",
    "отправить письмо",
    "купить",
    "оплати",
    "пароль",
    "банков",
    "финанс",
    "настройки системы",
    "установи",
    "установить",
    "терминал",
    "командную строку",
    "powershell",
    "сообщение от моего имени",
)


@dataclass(slots=True)
class AssistantConfig:
    wake_words: tuple[str, ...] = ("ассистент", "помощник")
    command_prefixes: tuple[str, ...] = (
        "сделай",
        "выполни",
        "открой",
        "запусти",
        "напиши",
        "найди",
    )
    screenshots_dir: Path = Path("screenshots")
    notes_dir: Path = Path("notes")
    use_vosk_offline: bool = True
    vosk_model_path: Path = Path("models") / "vosk-model-small-ru-0.22"
    allow_terminal_commands: bool = False
    dangerous_keywords: tuple[str, ...] = field(default_factory=lambda: DANGEROUS_KEYWORDS)

    def ensure_dirs(self, directories: Iterable[Path] | None = None) -> None:
        paths = list(directories) if directories else [self.screenshots_dir, self.notes_dir]
        for path in paths:
            path.mkdir(parents=True, exist_ok=True)
