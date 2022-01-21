from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Literal

from app.data import DEFAULT_DATA

Char = Literal[
    "а",
    "б",
    "в",
    "г",
    "д",
    "е",
    "ё",
    "ж",
    "з",
    "и",
    "й",
    "к",
    "л",
    "м",
    "н",
    "о",
    "п",
    "р",
    "с",
    "т",
    "у",
    "ф",
    "х",
    "ц",
    "ч",
    "ш",
    "щ",
    "ъ",
    "ы",
    "ь",
    "э",
    "ю",
    "я",
]
ANY_CHAR = r"[а-яё]"


@dataclass
class Source:
    data: tuple[str, ...] = field(default_factory=tuple)


DEFAULT_SOURCE = Source(DEFAULT_DATA)


class Status(Enum):
    black = auto()
    yellow = auto()
    green = auto()

    @classmethod
    def by_color(cls, color_code: str) -> Status:
        statuses_by_color = {
            "B": cls.black,
            "Y": cls.yellow,
            "G": cls.green,
        }
        return statuses_by_color.get(color_code)


@dataclass
class Cell:
    char: Char
    status: Status


@dataclass
class Position:
    defined_char: Char = None
    forbidden_chars: list[str, ...] = field(default_factory=list)

    @property
    def pattern(self) -> str:
        if self.defined_char:
            return self.defined_char

        if self.forbidden_chars:
            return f"[^{''.join(sorted(set(self.forbidden_chars)))}]"

        return ANY_CHAR

    def set_defined_char(self, char: Char) -> None:
        if char not in self.forbidden_chars:
            self.defined_char = char
        else:
            raise ValueError(f"The provided char '{char}' is in the list of forbidden chars")

    def add_forbidden_char(self, char: Char) -> None:
        if char not in self.forbidden_chars:
            self.forbidden_chars.append(char)


@dataclass
class Iteration:
    cell_1: Cell
    cell_2: Cell
    cell_3: Cell
    cell_4: Cell
    cell_5: Cell

    @property
    def cells(self) -> tuple[Cell, ...]:
        return self.cell_1, self.cell_2, self.cell_3, self.cell_4, self.cell_5


@dataclass
class Game:
    absent_chars: list[Char, ...] = field(default_factory=list)
    position_1: Position = field(default_factory=Position)
    position_2: Position = field(default_factory=Position)
    position_3: Position = field(default_factory=Position)
    position_4: Position = field(default_factory=Position)
    position_5: Position = field(default_factory=Position)

    @property
    def present_chars(self) -> tuple[Char, ...]:
        chars = []
        for pos in self.positions:
            chars.extend(pos.forbidden_chars)
            if pos.defined_char:
                chars.append(pos.defined_char)
        return tuple(sorted(set(chars)))

    @property
    def positions(self) -> tuple[Position, ...]:
        return (
            self.position_1,
            self.position_2,
            self.position_3,
            self.position_4,
            self.position_5,
        )

    @property
    def pattern(self) -> str:
        return f"^{''.join([position.pattern for position in self.positions])}$"

    def _add_absent_char(self, char: Char) -> None:
        if char not in self.absent_chars + list(self.present_chars):
            self.absent_chars.append(char)

    def add_iteration(self, iteration: Iteration) -> None:
        for pos, cell in zip(self.positions, iteration.cells):

            if cell.status == Status.black:
                self._add_absent_char(cell.char)

            elif cell.status == Status.yellow:
                pos.add_forbidden_char(cell.char)

            elif cell.status == Status.green:
                pos.set_defined_char(cell.char)

    def import_user_data(self, user_data: dict) -> None:
        for word, status in user_data.items():
            cells_data = zip(word, status)
            cells = [Cell(char, Status.by_color(color)) for char, color in cells_data]
            self.add_iteration(Iteration(*cells))

    def _word_is_suitable(self, word: str) -> bool:
        """
        Check the following conditions:
            all present chars exist in current word,
            all absent chars are not in current word,
            current word matches existing pattern
        :param word:
        :return:
        """

        present_chars_check = all(str(item) in word for item in self.present_chars)
        absent_chars_check = all(str(item) not in word for item in self.absent_chars)
        pattern_check = bool(re.match(self.pattern, word))
        return pattern_check and present_chars_check and absent_chars_check

    def get_suggestions(self, source: Source = DEFAULT_SOURCE) -> tuple[str, ...]:
        return tuple(filter(self._word_is_suitable, source.data))
