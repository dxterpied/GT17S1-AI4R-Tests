# Scenario class for testing etc.

# Apparently you can't import from a parent directory in python... Who knew?
# I guess this class needs to be in the same directory as the scenarios...

import re


class TestScenario:

    def __init__(self, name, warehouse, todo, benchmark_a=-1, benchmark_b=-1, benchmark_c=-1):

        self.name = name
        self.warehouse = warehouse
        self.todo = todo
        self.benchmarkA = benchmark_a
        self.benchmarkB = benchmark_b
        self.benchmarkC = benchmark_c

    def validate(self):

        # ensure that all properties are set to correct types
        if not isinstance(self.name, basestring):
            return False
        if not (isinstance(self.warehouse, list) and isinstance(self.warehouse[0], list) and isinstance(
                self.warehouse[0][0], basestring)):
            return False
        if self.benchmarkA < 0 or self.benchmarkB < 0 or self.benchmarkC < 0:
            return False

        # ensure that all rows and columns are consistently sized
        height = len(self.warehouse)
        width = len(self.warehouse[0])

        for row in range(height):
            if len(self.warehouse[row]) != width:
                return False

        # ensure that all cells have a valid symbol in
        for row in range(height):
            for column in range(width):
                symbol = self.warehouse[row][column]
                if len(symbol) != 1 and not re.match(r'^[a-zA-Z0-9@.#]*$', symbol, re.M):
                    return False

                    # TODO - check symbol not in use already

        # ensure todo is valid and exists in grid
        # TODO

        # ensure that problem is 'generally' solvable
        # TODO?

        return True
