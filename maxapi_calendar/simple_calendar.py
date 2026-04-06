import calendar
from datetime import datetime, timedelta

from maxapi.types import ButtonsPayload
from maxapi.types.updates.message_callback import MessageCallback
from maxapi.utils.inline_keyboard import InlineKeyboardBuilder
from maxapi.types.attachments.buttons import CallbackButton

from .schemas import SimpleCalendarCallback, SimpleCalAct, highlight, superscript
from .common import GenericCalendar


class SimpleCalendar(GenericCalendar):

    @property
    def _ignore_payload(self) -> str:
        return SimpleCalendarCallback.make(act=SimpleCalAct.ignore).pack()

    async def start_calendar(
        self,
        year: int = datetime.now().year,
        month: int = datetime.now().month,
    ) -> "ButtonsPayload":
        today = datetime.now()
        now_weekday = self._labels.days_of_week[today.weekday()]
        now_month, now_year, now_day = today.month, today.year, today.day

        def highlight_month() -> str:
            month_str = self._labels.months[month - 1]
            if now_month == month and now_year == year:
                return highlight(month_str)
            return month_str

        def highlight_weekday(weekday: str) -> str:
            if now_month == month and now_year == year and now_weekday == weekday:
                return highlight(weekday)
            return weekday

        def format_day_string(day: int) -> str:
            date_to_check = datetime(year, month, day)
            if self.min_date and date_to_check < self.min_date:
                return superscript(str(day))
            if self.max_date and date_to_check > self.max_date:
                return superscript(str(day))
            return str(day)

        def highlight_day(day: int) -> str:
            day_string = format_day_string(day)
            if now_month == month and now_year == year and now_day == day:
                return highlight(day_string)
            return day_string

        builder = InlineKeyboardBuilder()

        builder.row(
            CallbackButton(
                text="<<",
                payload=SimpleCalendarCallback.make(
                    act=SimpleCalAct.prev_y, year=year, month=month, day=1
                ).pack(),
            ),
            CallbackButton(
                text=str(year) if year != now_year else highlight(year),
                payload=self._ignore_payload,
            ),
            CallbackButton(
                text=">>",
                payload=SimpleCalendarCallback.make(
                    act=SimpleCalAct.next_y, year=year, month=month, day=1
                ).pack(),
            ),
        )

        builder.row(
            CallbackButton(
                text="<",
                payload=SimpleCalendarCallback.make(
                    act=SimpleCalAct.prev_m, year=year, month=month, day=1
                ).pack(),
            ),
            CallbackButton(
                text=highlight_month(),
                payload=self._ignore_payload,
            ),
            CallbackButton(
                text=">",
                payload=SimpleCalendarCallback.make(
                    act=SimpleCalAct.next_m, year=year, month=month, day=1
                ).pack(),
            ),
        )

        builder.row(
            *[
                CallbackButton(
                    text=highlight_weekday(weekday),
                    payload=self._ignore_payload,
                )
                for weekday in self._labels.days_of_week
            ]
        )

        month_calendar = calendar.monthcalendar(year, month)
        last_day = 1

        for week in month_calendar:
            row_buttons = []
            for day in week:
                if day == 0:
                    row_buttons.append(
                        CallbackButton(text="\u200b", payload=self._ignore_payload)
                    )
                else:
                    last_day = day
                    row_buttons.append(
                        CallbackButton(
                            text=highlight_day(day),
                            payload=SimpleCalendarCallback.make(
                                act=SimpleCalAct.day, year=year, month=month, day=day
                            ).pack(),
                        )
                    )
            builder.row(*row_buttons)

        builder.row(
            CallbackButton(
                text=self._labels.cancel_caption,
                payload=SimpleCalendarCallback.make(
                    act=SimpleCalAct.cancel, year=year, month=month, day=last_day
                ).pack(),
            ),
            CallbackButton(text="\u200b", payload=self._ignore_payload),
            CallbackButton(
                text=self._labels.today_caption,
                payload=SimpleCalendarCallback.make(
                    act=SimpleCalAct.today, year=year, month=month, day=last_day
                ).pack(),
            ),
        )

        return builder.as_markup()

    async def _update_calendar(
        self, event: MessageCallback, with_date: datetime
    ) -> None:
        if event.message is not None:
            new_markup = await self.start_calendar(
                int(with_date.year), int(with_date.month)
            )
            await event.message.edit(attachments=[new_markup])

    async def process_selection(
        self,
        event: MessageCallback,
        data: SimpleCalendarCallback,
    ) -> tuple[bool, datetime | None]:
        return_data = (False, None)
        act = data.act_enum

        if act == SimpleCalAct.ignore:
            await event.answer()
            return return_data

        temp_date = datetime(data.year_int(), data.month_int(), 1)

        if act == SimpleCalAct.day:
            return await self.process_day_select(data, event)

        if act == SimpleCalAct.prev_y:
            await self._update_calendar(
                event, datetime(data.year_int() - 1, data.month_int(), 1)
            )
        elif act == SimpleCalAct.next_y:
            await self._update_calendar(
                event, datetime(data.year_int() + 1, data.month_int(), 1)
            )
        elif act == SimpleCalAct.prev_m:
            await self._update_calendar(event, temp_date - timedelta(days=1))
        elif act == SimpleCalAct.next_m:
            await self._update_calendar(event, temp_date + timedelta(days=31))
        elif act == SimpleCalAct.today:
            now = datetime.now()
            if now.year != data.year_int() or now.month != data.month_int():
                await self._update_calendar(event, now)
            else:
                await event.answer()
        elif act == SimpleCalAct.cancel:
            if event.message is not None:
                await event.message.edit(attachments=[])

        return return_data
