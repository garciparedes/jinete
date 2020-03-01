import unittest
from copy import deepcopy

import jinete as jit
from tests.utils import (
    generate_one_position,
)


class TestServices(unittest.TestCase):

    def test_construction(self):
        position = generate_one_position()
        service = jit.Service(position)
        identifier_regex = r'(\w{8}(-\w{4}){3}-\w{12}?)'

        self.assertEqual(position, service.position)
        self.assertEqual(0, service.earliest)
        self.assertEqual(jit.MAX_FLOAT, service.latest)
        self.assertEqual(0, service.duration)
        self.assertRegex(service.identifier, identifier_regex)

    def test_construction_with_earliest(self):
        position = generate_one_position()
        earliest = 1800
        service = jit.Service(position, earliest=earliest)
        identifier_regex = r'(\w{8}(-\w{4}){3}-\w{12}?)'

        self.assertEqual(position, service.position)
        self.assertEqual(earliest, service.earliest)
        self.assertEqual(jit.MAX_FLOAT, service.latest)
        self.assertEqual(0, service.duration)
        self.assertRegex(service.identifier, identifier_regex)

    def test_construction_with_latest(self):
        position = generate_one_position()
        latest = 3600
        service = jit.Service(position, latest=latest)
        identifier_regex = r'(\w{8}(-\w{4}){3}-\w{12}?)'

        self.assertEqual(position, service.position)
        self.assertEqual(0, service.earliest)
        self.assertEqual(latest, service.latest)
        self.assertEqual(0, service.duration)
        self.assertRegex(service.identifier, identifier_regex)

    def test_construction_with_duration(self):
        position = generate_one_position()
        duration = 60
        service = jit.Service(position, duration=duration)
        identifier_regex = r'(\w{8}(-\w{4}){3}-\w{12}?)'

        self.assertEqual(position, service.position)
        self.assertEqual(0, service.earliest)
        self.assertEqual(jit.MAX_FLOAT, service.latest)
        self.assertEqual(duration, service.duration)
        self.assertRegex(service.identifier, identifier_regex)

    def test_construction_with_identifier(self):
        position = generate_one_position()
        identifier = '520311d4-90bc-48eb-a971-e616eb2f91ad'
        service = jit.Service(position, identifier=identifier)

        self.assertEqual(position, service.position)
        self.assertEqual(0, service.earliest)
        self.assertEqual(jit.MAX_FLOAT, service.latest)
        self.assertEqual(0, service.duration)
        self.assertEqual(identifier, service.identifier)

    def test_equals(self):
        position = generate_one_position()
        earliest = 1800
        latest = 3600
        duration = 60
        identifier = '520311d4-90bc-48eb-a971-e616eb2f91ad'

        one = jit.Service(position, earliest, latest, duration, identifier)
        two = jit.Service(position, earliest, latest, duration, identifier)
        self.assertEqual(one, two)

    def test_different_identifier(self):
        position = generate_one_position()
        earliest = 1800
        latest = 3600
        duration = 60

        one = jit.Service(position, earliest, latest, duration)
        two = jit.Service(position, earliest, latest, duration)
        self.assertNotEqual(one.identifier, two.identifier)

    def test_distance_to(self):
        one_position = generate_one_position()
        two_position = generate_one_position()
        one = jit.Service(one_position)
        two = jit.Service(two_position)
        self.assertEqual(one_position.distance_to(two_position), one.distance_to(two))

    def test_time_to(self):
        one_position = generate_one_position()
        two_position = generate_one_position()
        one = jit.Service(one_position)
        two = jit.Service(two_position)
        self.assertEqual(one_position.time_to(two_position), one.time_to(two))

    def test_tuple(self):
        position = generate_one_position()
        earliest = 1800
        latest = 3600
        duration = 60
        identifier = '520311d4-90bc-48eb-a971-e616eb2f91ad'

        service = jit.Service(position, earliest, latest, duration, identifier)

        raw = (
            ('position', position),
            ('earliest', earliest),
            ('latest', latest),
            ('duration', duration),
            ('identifier', identifier),
        )
        self.assertEqual(raw, tuple(service))

    def test_dict(self):
        position = generate_one_position()
        earliest = 1800
        latest = 3600
        duration = 60
        identifier = '520311d4-90bc-48eb-a971-e616eb2f91ad'

        service = jit.Service(position, earliest, latest, duration, identifier)

        raw = {
            'position': position,
            'earliest': earliest,
            'latest': latest,
            'duration': duration,
            'identifier': identifier,
        }
        self.assertEqual(raw, dict(service))

    def test_deepcopy(self):
        position = generate_one_position()
        copied_position = deepcopy(position)
        self.assertEqual(position, copied_position)


if __name__ == '__main__':
    unittest.main()
