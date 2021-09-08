from typing import List
from unittest import TestCase
from dataclasses import dataclass, field

import hodgepodge.classes


@dataclass(frozen=True)
class Pizza:
    crispy: bool = True
    tasty: bool = True
    toppings: List[str] = field(default_factory=list)
    special_instructions: List[str] = field(default_factory=list)

    def get_cheeses(self):
        return [name for name in self.toppings if 'cheese' in name]


class ClassTestCases(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pizza = Pizza(
            toppings=['broccoli', 'goat cheese', 'chicken', 'red pepper', 'pesto sauce'],
            special_instructions=[],
            crispy=False,
            tasty=True,
        )

    def test_get_attributes(self):
        expected = {'crispy', 'tasty', 'toppings', 'special_instructions', 'get_cheeses'}
        result = set(hodgepodge.classes.get_attributes(self.pizza))
        self.assertSetEqual(expected, result)

    def test_get_functions(self):
        expected = {'get_cheeses'}
        result = set(hodgepodge.classes.get_functions(self.pizza))
        self.assertSetEqual(expected, result)

    def test_get_variables(self):
        expected = {'toppings', 'crispy', 'tasty', 'special_instructions'}
        result = set(hodgepodge.classes.get_variables(self.pizza))
        self.assertSetEqual(expected, result)
