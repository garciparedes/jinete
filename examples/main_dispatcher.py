import logging
from functools import partial
from pathlib import Path

import jinete as jit

logger = logging.getLogger(__name__)

BASE_PATH = Path(__file__).parents[1]
DATASETS_PATH = BASE_PATH / 'res' / 'datasets'


def main():
    logger.info('Starting...')

    file_path = DATASETS_PATH / 'hashcode' / 'a_example.in'
    loader = jit.FileLoader(file_path)

    dispatcher = jit.StaticDispatcher(
        partial(jit.FileLoader, file_path=file_path),
        jit.NaiveAlgorithm,
        partial(jit.PromptStorer, formatter_cls=jit.ColumnarStorerFormatter),
    )

    dispatcher.run()

    logger.info('Finished...')


if __name__ == '__main__':
    main()
