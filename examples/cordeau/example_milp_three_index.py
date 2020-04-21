import logging
from pathlib import (
    Path,
)

import coloredlogs
import jinete as jit
import pulp as lp

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
        algorithm=jit.MilpAlgorithm,
        algorithm_kwargs={
            # 'solver': lp.XPRESS(msg=1, path=str(BASE_PATH / 'tmp' / 'xpressmp' / 'bin' / 'optimizer')),
            # 'solver': lp.GUROBI_CMD(msg=1),
            # 'solver': lp.CPLEX_CMD(msg=1, path=str(BASE_PATH / 'tmp' / 'cplex' / 'bin' / 'x86-64_osx' / 'cplex')),
            "solver": lp.SCIP(msg=1),
            # 'solver' :lp.PULP_CBC_CMD(msg=1, threads=4),
        },
        storer=jit.StorerSet,
        storer_kwargs={"storer_cls_set": {jit.PromptStorer, jit.GraphPlotStorer}},
    )
    result = solver.solve()  # noqa

    logger.info("Finished...")


if __name__ == "__main__":
    main()
