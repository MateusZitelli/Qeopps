#Qeopps
> *(Q)eopps is an (e)volutionary (o)ptimizer for (p)arallel (p)rogram(s)*

Qeopps is a tool to optimize parallel programs written in C with posix threads,
positioning and setting the granularity of different transactions.

The optimization is made with genetic algorithms, with the solutions represented
as a table with transactions and their position in the code. The code itself is
parsed and represented as a syntax tree, facilitating the placement of
transactions in the program.

The regions to be optimized is defined adding a custom tag in the C code.
For each generation a version of the original code is generated with the
transactions represented in each table in the population. This code is then sent
with compilation params to a fitness server which will be running in the desired
archteture, this server will compile and then returns the runtime of the
solution program, each runtime is used as the fitness of the solution.

This tool is not ready yet and presents a lot of bugs, but can be used to
optimize the positioning and granularity of: 
- [x] Mutex locks
- [ ] Transactional memory blocks
- [ ] Semaphores

## Usage
First you must change the configuration file ```src/client/test.cfg``` with your
preferences.

Then run the fitness server:
```sh
$ cd src/fitness_server
$ python server.py
```

And then the client
```sh
$ cd src/client
$ python main.py
```

After *reaching* the maximum generations number defined in the configuration file,
the solutions obtained in the last generation will be available in the directory
defined as ```population_programs_dir``` in the configuration.


*Under heavy development.*
