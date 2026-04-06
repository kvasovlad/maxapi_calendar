from enum import Enum
from typing import Optional

from pydantic import BaseModel, conlist, Field

from maxapi.filters.callback_payload import CallbackPayload


class SimpleCalAct(str, Enum):
    ignore   = 'IGNORE'
    prev_y   = 'PREV-YEAR'
    next_y   = 'NEXT-YEAR'
    prev_m   = 'PREV-MONTH'
    next_m   = 'NEXT-MONTH'
    cancel   = 'CANCEL'
    today    = 'TODAY'
    day      = 'DAY'


class DialogCalAct(str, Enum):
    ignore  = 'IGNORE'
    set_y   = 'SET-YEAR'
    set_m   = 'SET-MONTH'
    prev_y  = 'PREV-YEAR'
    next_y  = 'NEXT-YEAR'
    cancel  = 'CANCEL'
    start   = 'START'
    day     = 'SET-DAY'


class SimpleCalendarCallback(CallbackPayload, prefix="simple_calendar"):
    act:   str
    year:  Optional[str] = None
    month: Optional[str] = None
    day:   Optional[str] = None

    @classmethod
    def make(
        cls,
        act: SimpleCalAct,
        year: Optional[int] = None,
        month: Optional[int] = None,
        day: Optional[int] = None,
    ) -> "SimpleCalendarCallback":
        return cls(
            act=act.value,
            year=str(year) if year is not None else "",
            month=str(month) if month is not None else "",
            day=str(day) if day is not None else "",
        )

    @property
    def act_enum(self) -> SimpleCalAct:
        return SimpleCalAct(self.act)

    def year_int(self) -> Optional[int]:
        return int(self.year) if self.year else None

    def month_int(self) -> Optional[int]:
        return int(self.month) if self.month else None

    def day_int(self) -> Optional[int]:
        return int(self.day) if self.day else None


class CalendarLabels(BaseModel):

    days_of_week: conlist(str, max_length=7, min_length=7) = [
        "Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"
    ]
    months: conlist(str, max_length=12, min_length=12) = [
        "Jan", "Feb", "Mar", "Apr", "May", "Jun",
        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec",
    ]
    cancel_caption: str = Field(default="Отмена", description="Подпись кнопки Отмена")
    today_caption:  str = Field(default="Сегодня",  description="Подпись кнопки Сегодня")


HIGHLIGHT_FORMAT = "[{}]"


def highlight(text) -> str:
    return HIGHLIGHT_FORMAT.format(text)


def superscript(text: str) -> str:
    normal  = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+-=()"
    super_s = "ᴬᴮᶜᴰᴱᶠᴳᴴᴵᴶᴷᴸᴹᴺᴼᴾQᴿˢᵀᵁⱽᵂˣʸᶻᵃᵇᶜᵈᵉᶠᵍʰᶦʲᵏˡᵐⁿᵒᵖ۹ʳˢᵗᵘᵛʷˣʸᶻ⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾"
    return "".join(super_s[normal.index(c)] if c in normal else c for c in text)
