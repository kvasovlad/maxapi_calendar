"""
maxapi_calendar — inline-календарь для ботов мессенджера MAX на базе maxapi.

Порт библиотеки aiogram_calendar (https://github.com/noXplode/aiogram_calendar)
под Python-библиотеку maxapi (https://love-apples.github.io/maxapi/).

Экспортируемые имена повторяют оригинал, чтобы упростить миграцию:

    from maxapi_calendar import (
        SimpleCalendar,
        SimpleCalendarCallback,
        DialogCalendar,
        DialogCalendarCallback,
        get_user_locale,
    )
"""

from .simple_calendar import SimpleCalendar
from .dialog_calendar import DialogCalendar
from .schemas import (
    SimpleCalendarCallback,
    DialogCalendarCallback,
    CalendarLabels,
    SimpleCalAct,
    DialogCalAct,
)
from .common import get_user_locale

__all__ = [
    "SimpleCalendar",
    "SimpleCalendarCallback",
    "DialogCalendar",
    "DialogCalendarCallback",
    "CalendarLabels",
    "SimpleCalAct",
    "DialogCalAct",
    "get_user_locale",
]
