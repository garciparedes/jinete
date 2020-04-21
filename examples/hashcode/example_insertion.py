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

    FILES = {
        "a": "a_example.in",
        "b": "b_should_be_easy.in",
        "c": "c_no_hurry.in",
        "d": "d_metropolis.in",
        "e": "e_high_bonus.in",
    }

    file_path = DATASETS_PATH / "hashcode" / FILES["b"]

    solver = jit.Solver(
        loader_kwargs={"file_path": file_path, "formatter_cls": jit.HashCodeLoaderFormatter},
        algorithm=jit.InsertionAlgorithm,
        algorithm_kwargs={"criterion": jit.HashCodeRouteCriterion, "neighborhood_max_size": None},
    )
    result = solver.solve()  # noqa

    logger.info("Finished...")


if __name__ == "__main__":
    main()
