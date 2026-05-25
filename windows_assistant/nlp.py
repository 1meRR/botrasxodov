from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(slots=True)
class ParsedCommand:
    intent: str
    payload: dict[str, str]


class CommandParser:
    def parse(self, text: str) -> ParsedCommand:
        t = text.strip().lower()

        if t.startswith("открой сайт "):
            return ParsedCommand("open_website", {"url": text[11:].strip()})
        if t.startswith("открой ") or t.startswith("запусти "):
            app = text.split(" ", 1)[1].strip()
            return ParsedCommand("open_app", {"app": app})
        if t.startswith("напечатай ") or t.startswith("введи "):
            return ParsedCommand("type_text", {"text": text.split(" ", 1)[1].strip()})
        if t.startswith("нажми "):
            keys = re.split(r"\s*\+\s*|\s+", text.split(" ", 1)[1].strip())
            return ParsedCommand("press_keys", {"keys": ",".join(keys)})
        if t.startswith("перемести мышь "):
            coords = re.findall(r"\d+", t)
            if len(coords) >= 2:
                return ParsedCommand("move_mouse", {"x": coords[0], "y": coords[1]})
        if "скриншот" in t:
            return ParsedCommand("screenshot", {})
        if t.startswith("создай файл "):
            rest = text[len("создай файл "):]
            if ":" in rest:
                name, content = rest.split(":", 1)
            else:
                name, content = rest, ""
            return ParsedCommand("create_note", {"filename": name.strip(), "content": content.strip()})
        if t.startswith("найди файл "):
            return ParsedCommand("search_file", {"query": text[len("найди файл "):].strip()})
        if t.startswith("команда "):
            return ParsedCommand("run_command", {"command": text[len("команда "):].strip()})
        if t.startswith("ответь ") or t.startswith("вопрос "):
            question = text.split(" ", 1)[1].strip()
            return ParsedCommand("answer", {"question": question})

        return ParsedCommand("unknown", {"raw": text})
