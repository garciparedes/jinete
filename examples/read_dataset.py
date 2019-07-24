from pathlib import Path

import jinete as jit

BASE_PATH = Path(__file__).parents[1]
DATASETS_PATH = BASE_PATH / 'res' / 'datasets'


def main():
    file_path = DATASETS_PATH / 'hashcode' / 'a_example.in'
    loader = jit.FileLoader(file_path)

    print(f'Surface: \n  {loader.surface}')

    print(f'Vehicles: \n  {loader.fleet}')

    trips = "\n  ".join(map(str, loader.trips))
    print(f'Trips: \n  {trips}')


if __name__ == '__main__':
    main()
