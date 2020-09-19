import logging
from pathlib import (
    Path,
)

import coloredlogs
import jinete as jit

level = logging.INFO
logging.basicConfig(level=level)
coloredlogs.install(level=level)

logger = logging.getLogger(__name__)

BASE_PATH = Path(__file__).parents[2]
DATASETS_PATH = BASE_PATH / "res" / "datasets"


def main():
    logger.info("Starting...")

    file_path = DATASETS_PATH / "cordeau-laporte" / "a2-16.txt"

    solver = jit.Solver(
        loader_kwargs={"file_path": file_path},
        algorithm=jit.GraspAlgorithm,
        algorithm_kwargs={"first_solution_kwargs": {"episodes": 1, "randomized_size": 2}, "episodes": 5},
        storer=jit.StorerSet,
        storer_kwargs={"storer_cls_set": {jit.PromptStorer, jit.GraphPlotStorer}},
    )
    result = solver.solve()  # noqa

    logger.info("Finished...")


if __name__ == "__main__":
    main()
