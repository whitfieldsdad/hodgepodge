import hodgepodge.types
import hodgepodge.hashing
import unittest


class Class:
    pass


class IterableClass:
    def __iter__(self):
        for v in [1, 2, 3]:
            yield v


class TypeTestCases(unittest.TestCase):
    def test_select_from_dict(self):
        data = {
            'id': 'a4eaaf05-da54-4e87-bf84-ea4c17bd88f3',
            'name': 'Mary Poppins',
        }
        keys = ['id']
        expected = {
            'id': 'a4eaaf05-da54-4e87-bf84-ea4c17bd88f3'
        }
        result = hodgepodge.types.select_from_dict(data=data, keys=keys)
        self.assertEqual(expected, result)

    def test_select_from_dict_stream(self):
        rows = [
            {
                'id': 'a4eaaf05-da54-4e87-bf84-ea4c17bd88f3',
                'name': 'Mary Poppins',
            }
        ]
        keys = ['id']
        expected = [
            {
                'id': 'a4eaaf05-da54-4e87-bf84-ea4c17bd88f3'
            }
        ]
        result = list(hodgepodge.types.select_from_dict_stream(rows=rows, keys=keys))
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
