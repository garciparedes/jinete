import unittest
from uuid import UUID

from jinete import (
    XYPosition,
)


class TestPositions(unittest.TestCase):

    def test_xy_position(self):
        position = XYPosition(lat=3, lon=4)
        self.assertIsInstance(position.uuid, UUID)
        self.assertEqual(3, position.lat)
        self.assertEqual(4, position.lon)


if __name__ == '__main__':
    unittest.main()
