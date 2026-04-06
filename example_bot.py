import asyncio
import logging

from maxapi import Bot, Dispatcher
from maxapi.types import MessageCreated
from maxapi.types.updates.message_callback import MessageCallback
from maxapi.types import Command
from maxapi.utils.inline_keyboard import InlineKeyboardBuilder
from maxapi.types.attachments.buttons import CallbackButton

from maxapi_calendar import (
    SimpleCalendar,
    SimpleCalendarCallback,
    get_user_locale,
)

logging.basicConfig(level=logging.INFO)

bot = Bot(token="paste-your-token-here")
dp = Dispatcher()


@dp.message_created(Command("start"))
async def cmd_start(event: MessageCreated):
    builder = InlineKeyboardBuilder()
    builder.row(
        CallbackButton(text="Simple Calendar", payload="open_simple"),
        CallbackButton(text="Dialog Calendar", payload="open_dialog"),
    )
    await event.message.answer(
        text="Привет! Выберите тип календаря:",
        attachments=[builder.as_markup()],
    )


@dp.message_callback(SimpleCalendarCallback.filter())
async def process_simple_calendar(event: MessageCallback, payload: SimpleCalendarCallback):
    locale_str = await get_user_locale(event.user_locale)
    selected, date = await SimpleCalendar(locale=locale_str).process_selection(event, payload)

    if selected:
        await event.message.answer(
            text=f"✅ Вы выбрали дату: {date.strftime('%d.%m.%Y')}",
        )


@dp.message_callback()
async def open_simple_calendar(event: MessageCallback):
    if event.callback.payload != "open_simple":
        return

    locale_str = await get_user_locale(event.user_locale)
    markup = await SimpleCalendar(locale=locale_str).start_calendar()
    await event.message.answer(
        text="Выберите дату (Simple Calendar):",
        attachments=[markup],
    )
    await event.answer()


async def main():
    await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    asyncio.run(main())
