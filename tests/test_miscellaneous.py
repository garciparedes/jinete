import unittest

import jinete as jit


class TestMiscellaneous(unittest.TestCase):

    def test_version(self):
        self.assertIsInstance(jit.__version__, str)
        self.assertIsInstance(jit.VERSION, tuple)
        for value in jit.VERSION:
            self.assertIsInstance(value, int)
        self.assertEqual(jit.__version__, '.'.join(map(str, jit.VERSION)))


if __name__ == '__main__':
    unittest.main()
