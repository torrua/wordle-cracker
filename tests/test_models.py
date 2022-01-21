# -*- coding:utf-8 -*-
"""Test models"""

import os
import sys

import pytest

from app.models import Source, Status, Cell, Position, Iteration, Game

sys.path.insert(0, "%s/../" % os.path.dirname(os.path.abspath(__file__)))


class TestStatus:

    def test_status(self):
        assert Status.__dict__.get('_member_names_') == ['black', 'yellow', 'green']

    @staticmethod
    def test_by_color():
        assert Status.by_color("B") == Status.black
        assert Status.by_color("Y") == Status.yellow
        assert Status.by_color("G") == Status.green


class TestCell:

    @staticmethod
    def test_is_instance():
        cell = Cell(char='а', status=Status.yellow)

        assert isinstance(cell, Cell)
        assert cell.status == Status.yellow
        assert cell.char == 'а'
        assert list(cell.__dict__.keys()) == ['char', 'status']


class TestPosition:

    @staticmethod
    def test_is_instance():
        pos = Position(defined_char='а')

        assert isinstance(pos, Position)
        assert pos.defined_char == 'а'
        assert list(pos.__dict__.keys()) == ['defined_char', 'forbidden_chars']

    @staticmethod
    def test_pattern():
        pos = Position(defined_char='а')
        assert pos.pattern == 'а'

        pos = Position(forbidden_chars=['т', 'е', 'с', ])
        assert pos.pattern == '[^ест]'

        pos = Position()
        assert pos.pattern == r"[а-яё]"

    @staticmethod
    def test_set_defined_char():
        pos = Position(forbidden_chars=['т', 'е', 'с', ])

        with pytest.raises(ValueError) as _:
            pos.set_defined_char('е')

        pos.set_defined_char('к')
        assert pos.pattern == 'к'

    @staticmethod
    def test_add_forbidden_char():
        pos = Position(forbidden_chars=['т', 'е', 'с', ])
        pos.add_forbidden_char("е")
        assert pos.pattern == '[^ест]'

        pos.add_forbidden_char("р")
        assert pos.pattern == '[^ерст]'


class TestIteration:
    cells = (
        Cell("л", Status.black), Cell("о", Status.black),
        Cell("д", Status.black), Cell("к", Status.black),
        Cell("а", Status.black),)

    iteration = Iteration(*cells)

    def test_is_instance(self):
        assert isinstance(self.iteration, Iteration)
        assert self.iteration.cell_1 == self.cells[0]
        assert list(self.iteration.__dict__.keys()) == [
            'cell_1', 'cell_2', 'cell_3', 'cell_4', 'cell_5', ]

    def test_cells(self):
        assert self.iteration.cells == self.cells


class TestGame:

    absent_chars = ['щ', 'у', ],
    positions = (
        Position(defined_char='л'),
        Position(forbidden_chars=['о', 'с', ]),
        Position(defined_char='с'),
        Position(forbidden_chars=['р', ]),
        Position(forbidden_chars=['т', ]), )

    data = [absent_chars, *positions]

    @staticmethod
    def test_is_instance():
        g = Game()

        assert isinstance(g, Game)
        assert list(g.__dict__.keys()) == [
            'absent_chars', 'position_1', 'position_2',
            'position_3', 'position_4', 'position_5', ]
        assert g.absent_chars == list()
        assert isinstance(g.position_1, Position)

    def test_present_chars(self):
        game = Game(*self.data)
        assert game.present_chars == ('л', 'о', 'р', 'с', 'т')

    def test_positions(self):
        game = Game(*self.data)
        assert game.positions == self.positions

    def test_pattern(self):
        game = Game(*self.data)
        assert game.pattern == '^л[^ос]с[^р][^т]$'

    def test_add_absent_char(self):
        pass

    @staticmethod
    def test_add_iteration():
        g = Game()
        assert g.absent_chars == list()

        cells = (
            Cell("л", Status.black), Cell("о", Status.yellow),
            Cell("д", Status.green), Cell("к", Status.black),
            Cell("а", Status.yellow),)

        iteration = Iteration(*cells)
        g.add_iteration(iteration)

        assert g.absent_chars == ['л', 'к']

    def test_import_user_data(self):
        g = Game()
        user_data = {'ветка': 'BYYYB'}
        g.import_user_data(user_data)

        assert g.absent_chars == ["в", "а"]
        assert g.position_2.forbidden_chars == ["е", ]
        assert g.position_3.forbidden_chars == ["т", ]
        assert g.position_4.forbidden_chars == ["к", ]

    def test_word_is_suitable(self):
        game = Game(*self.data)
        assert game._word_is_suitable("лодка") is False
        assert game._word_is_suitable("лрсто") is True

    def test_get_suggestions(self):
        g = Game()
        user_data = {'ветка': 'BYYYB'}
        g.import_user_data(user_data)

        words = ('букет', 'крест', 'треск', 'висок', 'выкуп')
        source = Source(words)

        assert g.get_suggestions(source=source) == ('букет', 'крест', 'треск', )
