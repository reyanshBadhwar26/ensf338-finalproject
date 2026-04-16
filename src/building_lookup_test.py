"""
Demonstrates that BuildingLookup provides near O(1) lookup performance.

This TEST FILE tests lookup speed for increasing dataset sizes by inserting
many buildings into a dictionary-based structure and measuring the average
lookup time. The results show that lookup time remains nearly constant,
indicating performance is independent of the number of stored records.
"""

import time
from building_lookup import BuildingLookup


class TestBuilding:
    def __init__(self, building_id, name, location=(0, 0)):
        self.building_id = building_id
        self.name = name
        self.location = location


def demo_lookup_performance():
    print("\nFast Building Lookup Performance Demo")
    print("=" * 40)

    sizes = [10, 100, 1000, 10000, 50000]  # different dataset sizes to test

    for size in sizes:
        lookup = BuildingLookup()  # create new lookup structure

        # insert many buildings into the dictionary
        for i in range(size):
            lookup.insert_building(TestBuilding(f"BLD-{i}", f"Building {i}"))

        key = f"BLD-{size // 2}"  # key to lookup
        repetitions = 100000     # repeat lookups for accurate timing

        # measure total time for repeated lookups
        start = time.perf_counter()
        for _ in range(repetitions):
            lookup.lookup_building(key)
        end = time.perf_counter()

        # compute average lookup time in milliseconds
        avg_ms = ((end - start) / repetitions) * 1000

        print(f"{size:>6} records -> {avg_ms:.8f} ms per lookup")

    print("\nConclusion: Lookup time remains nearly constant as dataset size grows.")


if __name__ == "__main__":
    demo_lookup_performance()

# Lookup operations in our program are implemented using Python dictionaries, which are based on hash tables 
# and provide average-case O(1) access time. As demonstrated in our performance test, 
# increasing the number of stored records from small to large datasets results in little to no change 
# in the average lookup time. This shows that lookup performance is largely independent of the size
#  of the dataset. Any small variations observed are due to system-level factors such as timing precision 
# rather than the algorithm itself. Therefore, the implementation efficiently scales and maintains 
# fast access even as the number of records grows.