# Directory Hierarchy

* [examples](https://github.com/garciparedes/jinete/tree/master/examples/): Basic examples to start using the library.
* [jinete](https://github.com/garciparedes/jinete/tree/master/jinete/): The source code of the library.
  * [algorithms](https://github.com/garciparedes/jinete/tree/master/jinete/algorithms/): Contains the implementation of solving methods.
    * [exacts](https://github.com/garciparedes/jinete/tree/master/jinete/algorithms/exacts): Exact implementations based on linear programming and MILP solvers.
    * [heuristics](https://github.com/garciparedes/jinete/tree/master/jinete/algorithms/heuristics): Set of solving methods with reasonable space and time complexity.
      * [insertion](https://github.com/garciparedes/jinete/tree/master/jinete/algorithms/heuristics/insertion): Set of route generation methods.
        * [strategies](https://github.com/garciparedes/jinete/tree/master/jinete/algorithms/heuristics/insertion/strategies): Decision logic about how to insert trips.
        * [iterators](https://github.com/garciparedes/jinete/tree/master/jinete/algorithms/heuristics/insertion/strategies): Iteration logic related with trip insertions.
      * [local_search](https://github.com/garciparedes/jinete/tree/master/jinete/algorithms/heuristics/local_search): Set of route costs improvement methods. 
        * [strategies](https://github.com/garciparedes/jinete/tree/master/jinete/algorithms/heuristics/local_search/strategies): Decision logic about how to improve costs.
    * [metaheuristics](https://github.com/garciparedes/jinete/tree/master/jinete/algorithms/metaheuristics): Advanced solving methods built on top of heuristics.
    * [utils](https://github.com/garciparedes/jinete/tree/master/jinete/algorithms/utils): A set of functions to support the algorithms implementation.
  * [dispatchers](https://github.com/garciparedes/jinete/tree/master/jinete/dispatchers/): High level schedulers during the process of optimization (feeding with new trips, updating state, etc.).
  * [loaders](https://github.com/garciparedes/jinete/tree/master/jinete/loaders/): Entities whose responsibility is to provide problem instances.
    * [formatters](https://github.com/garciparedes/jinete/tree/master/jinete/loaders/formatters/): Parsing logic for problem instances.
  * [models](https://github.com/garciparedes/jinete/tree/master/jinete/models/): The set of classes which models problem instances, solutions, etc.
  * [storers](https://github.com/garciparedes/jinete/tree/master/jinete/storers/): Entities whose responsibility is to deliver problem solutions.
    * [formatters](https://github.com/garciparedes/jinete/tree/master/jinete/storers/formatters/): Parsing logic for problem solutions.
  * [solvers](https://github.com/garciparedes/jinete/tree/master/jinete/solvers.py): A set of abstractions to ease the launching process on external systems.
* [setup.py](https://github.com/garciparedes/jinete/tree/master/setup.py): The builder of this library.
* [tests](https://github.com/garciparedes/jinete/tree/master/tests/): The library tests.