from dataclasses import dataclass, field

import hodgepodge.types
import hodgepodge.hashing
import unittest


class Class:
    pass


@dataclass(frozen=True)
class Dataclass:
    id: int
    color: str = field(default="blue", init=False)


class IterableClass:
    def __iter__(self):
        for v in [1, 2, 3]:
            yield v


class TypeTestCases(unittest.TestCase):
    def test_get_nested_keys(self):
        data = {
            'id': 1,
            'name': 'Bob',
            'skills': [
                'magic'
            ],
            'favourite': {
                'sandwich': {
                    'toppings': [
                        'mayo', 'tomato', 'bacon', 'lettuce'
                    ]
                },
                'fruit': 'lemon',
            }
        }
        expected = {
            'id', 'name', 'skills', 'favourite', 'favourite.sandwich', 'favourite.sandwich.toppings', 'favourite.fruit'
        }
        result = hodgepodge.types.get_nested_keys(data)
        self.assertEqual(expected, result)

    def test_dict_to_dataclass_with_no_init_field(self):
        data = {
            'id': 123
        }
        result = hodgepodge.types.dict_to_dataclass(data, Dataclass)
        self.assertIsInstance(result, Dataclass)
        self.assertEqual(result.id, data['id'])
        self.assertEqual(result.color, 'blue')

    def test_dataclass_to_dict(self):
        data = Dataclass(id=123)
        result = hodgepodge.types.dataclass_to_dict(data)
        expected = {
            'id': 123,
            'color': 'blue'
        }
        self.assertEqual(expected, result)

    def test_is_iterable(self):
        for vector, expected in [
            (None, False),
            ([], True),
            ('', True),
            (b'', True),
            (bytearray(b''), True),
            (Class, False),
            (Class(), False),
            (IterableClass, False),
            (IterableClass(), True),
            (1, False),
        ]:
            with self.subTest(vector=vector, expected=expected):
                result = hodgepodge.types.is_iterable(vector)
                self.assertEqual(expected, result)

    def test_is_iterator(self):
        for vector, expected in [
            (None, False),
            ([], False),
            (iter([]), True),
            ('', False),
            (b'', False),
            (bytearray(b''), False),
            (Class, False),
            (Class(), False),
            (IterableClass, False),
            (IterableClass(), False),
            (iter(IterableClass()), True),
            (1, False),
        ]:
            with self.subTest(vector=vector, expected=expected):
                result = hodgepodge.types.is_iterator(vector)
                self.assertEqual(expected, result)

    def test_str_to_bool(self):
        for txt, expected in (
            ('y', True),
            ('yes', True),
            ('no', False),
            ('n', False),
            ('true', True),
            ('t', True),
            ('True', True),
            ('false', False),
            ('f', False),
            ('False', False),
        ):
            with self.subTest(txt=txt, expected=expected):
                result = hodgepodge.types.str_to_bool(txt)
                self.assertEqual(expected, result)

    def test_str_to_bytes(self):
        result = hodgepodge.types.str_to_bytes('hello')
        expected = b'hello'
        self.assertEqual(expected, result)

    def test_bytes_to_str(self):
        result = hodgepodge.types.bytes_to_str(b"hello")
        expected = "hello"
        self.assertEqual(expected, result)

    def test_dict_to_json(self):
        data = {
            'name': 'Tyler Fisher',
            'create_time': 1623683836.237236,
        }
        expected = '{"create_time": 1623683836.237236, "name": "Tyler Fisher"}'
        result = hodgepodge.types.dict_to_json(data, indent=None)
        self.assertEqual(expected, result)
