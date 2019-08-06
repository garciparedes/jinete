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
    loader = jit.FileLoader(file_path)

    dispatcher = jit.StaticDispatcher(
        partial(jit.FileLoader, file_path=file_path),
        jit.GreedyAlgorithm,
        partial(jit.PromptStorer, formatter_cls=jit.ColumnarStorerFormatter),
    )

    dispatcher.run()

    logger.info('Finished...')


if __name__ == '__main__':
    main()
