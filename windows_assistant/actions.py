from __future__ import annotations

import os
import subprocess
import webbrowser
from datetime import datetime
from pathlib import Path

import pyautogui
import pyperclip
from mss import mss
from PIL import Image


class ActionExecutor:
    def __init__(self, screenshots_dir: Path, notes_dir: Path, allow_terminal_commands: bool = False) -> None:
        self.screenshots_dir = screenshots_dir
        self.notes_dir = notes_dir
        self.allow_terminal_commands = allow_terminal_commands

    def open_website(self, url: str) -> str:
        if not url.startswith(("http://", "https://")):
            url = f"https://{url}"
        webbrowser.open(url)
        return f"Открываю сайт: {url}"

    def open_app(self, app_name: str) -> str:
        os.startfile(app_name)
        return f"Запускаю: {app_name}"

    def type_text(self, text: str) -> str:
        pyperclip.copy(text)
        pyautogui.hotkey("ctrl", "v")
        return "Текст вставлен в активное окно."

    def press_keys(self, *keys: str) -> str:
        pyautogui.hotkey(*keys)
        return f"Нажаты клавиши: {' + '.join(keys)}"

    def move_mouse(self, x: int, y: int) -> str:
        pyautogui.moveTo(x, y, duration=0.2)
        return f"Курсор перемещён в координаты ({x}, {y})."

    def screenshot(self) -> str:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        output = self.screenshots_dir / f"screen_{ts}.png"
        with mss() as sct:
            shot = sct.grab(sct.monitors[1])
            img = Image.frombytes("RGB", shot.size, shot.bgra, "raw", "BGRX")
            img.save(output)
        return f"Скриншот сохранён: {output}"

    def create_note(self, filename: str, content: str) -> str:
        safe_name = filename.replace("..", "_").replace("/", "_").replace("\\", "_")
        if not safe_name.endswith(".txt"):
            safe_name += ".txt"
        file_path = self.notes_dir / safe_name
        file_path.write_text(content, encoding="utf-8")
        return f"Файл создан: {file_path}"

    def search_file(self, query: str, root: str = "C:\\") -> str:
        query = query.lower()
        for base, _, files in os.walk(root):
            for file_name in files:
                if query in file_name.lower():
                    return f"Найден файл: {Path(base) / file_name}"
        return "Файл не найден."

    def run_safe_command(self, command: str) -> str:
        if not self.allow_terminal_commands:
            return "Выполнение команд в терминале отключено настройками безопасности."
        allowed_prefixes = ("dir", "echo", "whoami", "ipconfig", "systeminfo")
        if not command.lower().startswith(allowed_prefixes):
            return "Команда отклонена политикой безопасности."
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=20)
        out = result.stdout.strip() or result.stderr.strip() or "Команда выполнена без вывода."
        return out[:1000]
