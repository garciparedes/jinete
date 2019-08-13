import unittest
from uuid import UUID

import jinete as jit


class TestPositions(unittest.TestCase):

    def test_creation(self):
        dispatcher = jit.StaticDispatcher(
            jit.Loader,
            jit.Algorithm,
            jit.Storer,
        )
        self.assertEqual(dispatcher.loader_cls, jit.Loader)
        self.assertEqual(dispatcher.algorithm_cls, jit.Algorithm)
        self.assertEqual(dispatcher.storer_cls, jit.Storer)


if __name__ == '__main__':
    unittest.main()
