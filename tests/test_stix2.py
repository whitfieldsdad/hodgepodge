from unittest import TestCase
from hodgepodge.stix2 import MITRE_ATTACK_ICS_URL

import hodgepodge.stix2
import stix2


class Stix2TestCases(TestCase):
    def test_get_taxii_data_source(self):
        data_source = hodgepodge.stix2.get_taxii_data_source(url=MITRE_ATTACK_ICS_URL)
        self.assertIsInstance(data_source, stix2.TAXIICollectionSource)

    def test_get_object_by_id(self):
        data_source = hodgepodge.stix2.get_taxii_data_source(url=MITRE_ATTACK_ICS_URL)
        row = hodgepodge.stix2.get_object(
            data_source=data_source,
            object_id='intrusion-set--76d59913-1d24-4992-a8ac-05a3eb093f71',
        )
        self.assertIsInstance(row, dict)

    def test_get_objects_by_name(self):
        data_source = hodgepodge.stix2.get_taxii_data_source(url=MITRE_ATTACK_ICS_URL)
        rows = hodgepodge.stix2.get_objects(
            data_source=data_source,
            object_names=['Dragonfly 2.0']
        )
        self.assertIsInstance(rows, list)
        self.assertEqual(1, len(rows))

        expected = 'intrusion-set--76d59913-1d24-4992-a8ac-05a3eb093f71'
        result = rows[0]['id']
        self.assertEqual(expected, result)

    def test_get_objects_by_alias(self):
        data_source = hodgepodge.stix2.get_taxii_data_source(url=MITRE_ATTACK_ICS_URL)
        rows = hodgepodge.stix2.get_objects(
            data_source=data_source,
            object_names=['Berserk Bear'],
        )
        self.assertIsInstance(rows, list)
        self.assertEqual(1, len(rows))

        expected = 'intrusion-set--76d59913-1d24-4992-a8ac-05a3eb093f71'
        result = rows[0]['id']
        self.assertEqual(expected, result)

    def test_get_objects_by_external_id(self):
        data_source = hodgepodge.stix2.get_taxii_data_source(url=MITRE_ATTACK_ICS_URL)
        rows = hodgepodge.stix2.get_objects(
            data_source=data_source,
            object_external_ids=['G0074'],
        )
        self.assertIsInstance(rows, list)
        self.assertEqual(1, len(rows))

        expected = 'intrusion-set--76d59913-1d24-4992-a8ac-05a3eb093f71'
        result = rows[0]['id']
        self.assertEqual(expected, result)

    def test_get_objects_by_type(self):
        data_source = hodgepodge.stix2.get_taxii_data_source(url=MITRE_ATTACK_ICS_URL)
        rows = hodgepodge.stix2.get_objects(
            data_source=data_source,
            object_types=['intrusion-set'],
        )
        self.assertIsInstance(rows, list)
        self.assertGreater(len(rows), 0)

        expected = {'intrusion-set'}
        result = {row['type'] for row in rows}
        self.assertEqual(expected, result)
