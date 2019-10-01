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

    file_path = DATASETS_PATH / 'cordeau-laporte' / 'a2-16.txt'

    class MyLoader(jit.FileLoader):
        def __init__(self, *args, **kwargs):
            super().__init__(
                file_path=file_path,
                formatter_cls=jit.CordeauLaporteLoaderFormatter,
                *args, **kwargs,
            )

    class MyAlgorithm(jit.GraspAlgorithm):
        def __init__(self, *args, **kwargs):
            super().__init__(
                *args, **kwargs,
            )

    class MyStorer(jit.PromptStorer):
        def __init__(self, *args, **kwargs):
            super().__init__(
                formatter_cls=jit.ColumnarStorerFormatter,
                *args, **kwargs,
            )

    class MyStorerSet(jit.StorerSet):
        def __init__(self, *args, **kwargs):
            super().__init__(
                storer_cls_set={
                    MyStorer,
                    jit.GraphPlotStorer,
                },
                *args, **kwargs,
            )

    dispatcher = jit.StaticDispatcher(
        MyLoader,
        MyAlgorithm,
        MyStorerSet,
    )

    result = dispatcher.run()  # noqa

    logger.info('Finished...')


if __name__ == '__main__':
    main()
