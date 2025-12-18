"""Flip Flop puzzle 4, 2025: Beach Cleanup."""

import itertools

type Coordinate = tuple[int, int]


def parse_data(puzzle_input: str) -> list[Coordinate]:
    """Parse puzzle input."""
    return [
        (int(x), int(y))
        for line in puzzle_input.splitlines()
        for x, y in [line.split(",")]
    ]


def part1(coords: list[Coordinate]) -> int:
    """Solve part 1."""
    return sum(
        manhattan(prev, curr) for prev, curr in itertools.pairwise([(0, 0), *coords])
    )


def part2(coords: list[Coordinate]) -> int:
    """Solve part 2."""
    return sum(
        diagonal(prev, curr) for prev, curr in itertools.pairwise([(0, 0), *coords])
    )


def part3(coords: list[Coordinate]) -> int:
    """Solve part 3."""
    ordered_coords = sorted(coords, key=lambda pos: manhattan((0, 0), pos))
    return sum(
        diagonal(prev, curr)
        for prev, curr in itertools.pairwise([(0, 0), *ordered_coords])
    )


def manhattan(first: Coordinate, second: Coordinate) -> int:
    """Calculate the Manhattan distance between first and second."""
    (x1, y1), (x2, y2) = first, second
    return abs(x2 - x1) + abs(y2 - y1)


def diagonal(first: Coordinate, second: Coordinate) -> int:
    """Calculate the distance between first and second allowing diagonal steps."""
    (x1, y1), (x2, y2) = first, second
    return max(abs(x2 - x1), abs(y2 - y1))
