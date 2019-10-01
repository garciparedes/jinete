import logging
from pathlib import Path

import coloredlogs

import jinete as jit

level = logging.INFO
logging.basicConfig(level=level)
coloredlogs.install(level=level)

logger = logging.getLogger(__name__)

BASE_PATH = Path(__file__).parents[2]
DATASETS_PATH = BASE_PATH / 'res' / 'datasets'


def main():
    logger.info('Starting...')

    FILES = {
        'a': 'a_example.in',
        'b': 'b_should_be_easy.in',
        'c': 'c_no_hurry.in',
        'd': 'd_metropolis.in',
        'e': 'e_high_bonus.in',
    }

    file_path = DATASETS_PATH / 'hashcode' / FILES['b']

    class MyLoader(jit.FileLoader):
        def __init__(self, *args, **kwargs):
            super().__init__(
                file_path=file_path,
                formatter_cls=jit.HashCodeLoaderFormatter,
                *args, **kwargs,
            )

    class MyAlgorithm(jit.InsertionAlgorithm):
        def __init__(self, *args, **kwargs):
            super().__init__(
                neighborhood_max_size=None,
                criterion_cls=jit.HashCodePlannedTripCriterion,
                *args, **kwargs,
            )

    class MyStorer(jit.PromptStorer):
        def __init__(self, *args, **kwargs):
            super().__init__(
                formatter_cls=jit.ColumnarStorerFormatter,
                *args, **kwargs,
            )

    dispatcher = jit.StaticDispatcher(
        MyLoader,
        MyAlgorithm,
        MyStorer,
    )

    result = dispatcher.run()  # noqa

    logger.info('Finished...')


if __name__ == '__main__':
    main()
