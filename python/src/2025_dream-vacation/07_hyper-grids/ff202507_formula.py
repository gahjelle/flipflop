"""Flip Flop puzzle 7, 2025: Hyper Grids."""

import math

type Size = tuple[int, int]


def parse_data(puzzle_input: str) -> list[Size]:
    """Parse puzzle input."""
    return [
        (int(w), int(h))
        for line in puzzle_input.splitlines()
        for w, h in [line.split()]
    ]


def part1(sizes: list[Size]) -> int:
    """Solve part 1."""
    return sum(pascal(width - 1, height - 1) for width, height in sizes)


def part2(sizes: list[Size]) -> int:
    """Solve part 2."""
    return sum(pascal(width - 1, height - 1, width - 1) for width, height in sizes)


def part3(sizes: list[Size]) -> int:
    """Solve part 3."""
    return sum(pascal(*([size - 1] * num_dims)) for num_dims, size in sizes)


def pascal(*numbers: int) -> int:
    """Calculate Pascal's triangle-ish numbers."""
    return math.factorial(sum(numbers)) // math.prod(math.factorial(n) for n in numbers)
