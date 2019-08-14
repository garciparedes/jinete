import unittest

import jinete as jit


class TestHashCodeLoaderFormatter(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.data = (
            (3.0, 4.0, 2.0, 3.0, 2.0, 10.0),
            (0.0, 0.0, 1.0, 3.0, 2.0, 9.0),
            (1.0, 2.0, 1.0, 0.0, 0.0, 9.0),
            (2.0, 0.0, 2.0, 2.0, 0.0, 9.0),
        )

    def test_creation(self):
        formatter = jit.HashCodeLoaderFormatter(self.data)
        self.assertEqual(formatter.data, self.data)


if __name__ == '__main__':
    unittest.main()
