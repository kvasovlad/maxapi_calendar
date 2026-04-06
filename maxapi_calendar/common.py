import locale
from datetime import datetime

from maxapi.types.updates.message_callback import MessageCallback

from .schemas import CalendarLabels


CALENDAR_LABELS = {
    "en_US": {
        "days": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        "months": ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                   "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
    },
    "ru_RU": {
        "days": ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"],
        "months": ["Янв", "Фев", "Мар", "Апр", "Май", "Июн",
                   "Июл", "Авг", "Сен", "Окт", "Ноя", "Дек"],
    },
}

def get_locale_labels(locale_str: str) -> dict[str, list[str]]:
    return CALENDAR_LABELS.get(locale_str, CALENDAR_LABELS["en_US"])

async def get_user_locale(user_locale: str | None) -> str:
    if not user_locale:
        return "en_US"
    loc = user_locale.lower().replace("-", "_")
    return locale.locale_alias.get(loc, "en_US").split(".")[0]


class GenericCalendar:

    def __init__(
        self,
        locale: str | None = None,
        cancel_btn: str | None = None,
        today_btn: str | None = None,
        show_alerts: bool = False,
    ) -> None:
        self._labels = CalendarLabels()
        if locale:
            labels = get_locale_labels(locale)
            self._labels.days_of_week = labels["days"]
            self._labels.months = labels["months"]
        else:
            self._labels.days_of_week = CALENDAR_LABELS["en_US"]["days"]
            self._labels.months = CALENDAR_LABELS["en_US"]["months"]

        if cancel_btn:
            self._labels.cancel_caption = cancel_btn
        if today_btn:
            self._labels.today_caption = today_btn

        self.min_date: datetime | None = None
        self.max_date: datetime | None = None
        self.show_alerts: bool = show_alerts

    def set_dates_range(self, min_date: datetime, max_date: datetime) -> None:
        self.min_date = min_date
        self.max_date = max_date

    async def process_day_select(
        self, data, event: MessageCallback
    ) -> tuple[bool, datetime | None]:
        date = datetime(data.year_int(), data.month_int(), data.day_int())

        if self.min_date and self.min_date > date:
            await event.answer(
                notification=f'Дата должна быть не раньше {self.min_date.strftime("%d/%m/%Y")}',
            )
            return False, None

        if self.max_date and self.max_date < date:
            await event.answer(
                notification=f'Дата должна быть не позже {self.max_date.strftime("%d/%m/%Y")}',
            )
            return False, None

        if event.message is not None:
            await event.message.edit(attachments=[])

        return True, date
