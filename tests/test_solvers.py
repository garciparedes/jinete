import unittest
from pathlib import Path

import jinete as jit


class TestSolver(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.file_path = Path(__file__).parent / "res" / "problem-4.txt"

    def test_loader(self):
        solver = jit.Solver(loader=jit.FileLoader, loader_kwargs={"file_path": self.file_path,})
        loader_cls = solver._loader_cls
        self.assertTrue(issubclass(loader_cls, jit.FileLoader))

    def test_algorithm(self):
        solver = jit.Solver(loader_kwargs={"file_path": self.file_path,}, algorithm=jit.InsertionAlgorithm,)
        self.assertTrue(issubclass(solver._algorithm_cls, jit.InsertionAlgorithm))

    def test_storer(self):
        solver = jit.Solver(loader_kwargs={"file_path": self.file_path,}, storer=jit.PromptStorer,)
        self.assertTrue(issubclass(solver._storer_cls, jit.PromptStorer))

    def test_dispatcher(self):
        solver = jit.Solver(loader_kwargs={"file_path": self.file_path,}, dispatcher=jit.StaticDispatcher,)
        self.assertTrue(issubclass(solver._dispatcher_cls, jit.StaticDispatcher))
        self.assertIsInstance(solver._dispatcher, jit.StaticDispatcher)

    def test_solve(self):
        solver = jit.Solver(loader_kwargs={"file_path": self.file_path,},)

        self.assertIsInstance(solver.solve(), jit.Result)


if __name__ == "__main__":
    unittest.main()
