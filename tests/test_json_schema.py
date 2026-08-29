from unittest import TestCase
from hodgepodge import json_schema


class TestJsonSchema(TestCase):
    def test_get_json_schema_from_dicts(self):
        hosts = [
            {'ip_address': '192.168.1.1', 'hostname': 'a'},
            {'ip_address': '192.168.1.2', 'hostname': 'b'},
            {'ip_address': '192.168.1.3', 'hostname': 'c'},
        ]
        expected = {
            "$schema": "http://json-schema.org/schema#",
            "type": "object",
            "properties": {
                "ip_address": {
                    "type": "string"
                },
                "hostname": {
                    "type": "string"
                }
            },
            "required": [
                "hostname",
                "ip_address"
            ]
        }
        result = json_schema.get_json_schema_from_dicts(hosts)
        self.assertEqual(result, expected)
