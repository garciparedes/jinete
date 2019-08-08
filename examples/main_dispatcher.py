import logging
from functools import partial
from pathlib import Path

import jinete as jit

logging.basicConfig(
    level=logging.INFO
)

logger = logging.getLogger(__name__)

BASE_PATH = Path(__file__).parents[1]
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

    class MyStorer(jit.PromptStorer):
        def __init__(self, *args, **kwargs):
            super().__init__(
                formatter_cls=jit.HashCodeStorerFormatter,
                *args, **kwargs,
            )

    dispatcher = jit.StaticDispatcher(
        MyLoader,
        jit.GreedyAlgorithm,
        MyStorer,
    )

    result = dispatcher.run()

    logger.info('Finished...')


if __name__ == '__main__':
    main()
