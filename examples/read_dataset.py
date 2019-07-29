from pathlib import Path

import jinete as jit

BASE_PATH = Path(__file__).parents[1]
DATASETS_PATH = BASE_PATH / 'res' / 'datasets'


def main():
    file_path = DATASETS_PATH / 'hashcode' / 'a_example.in'
    loader = jit.FileLoader(file_path)

    print(f'Surface: \n  {loader.surface}')
    print(f'Fleet: \n  {loader.fleet}')
    print(f'Job: \n  {loader.job}')


if __name__ == '__main__':
    main()
