import asyncio
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import TOKEN
from utils import format_stats, format_today, save_expense


loop = asyncio.get_event_loop()
storage = MemoryStorage()
bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, loop=loop, storage=storage)


@dp.message_handler(commands=["start", "help"])
async def send_welcome(message: types.Message):
    text = [
        "Привет! Пиши расходы в формате:",
        "еда 150",
        "Команды:",
        "/today - за сегодня",
        "/stats - топ расходов",
    ]
    await message.answer("\n".join(text))


@dp.message_handler(commands=["today"])
async def handle_today(message: types.Message):
    data = format_today()
    await message.answer(data)


@dp.message_handler(commands=["stats"])
async def handle_stats(message: types.Message):
    data = format_stats()
    await message.answer(data)


@dp.message_handler()
async def handle_expense(message: types.Message):
    ok = save_expense(message.text)
    if ok:
        await message.answer("Записал")
    else:
        await message.answer("Не понял. Надо так: кофе 120")


def main():
    executor.start_polling(dp, skip_updates=True)


if __name__ == "__main__":
    main()
