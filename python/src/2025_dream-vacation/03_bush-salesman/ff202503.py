"""Flip Flop puzzle 3, 2025: Bush Salesman."""

import collections
from functools import cache

type Color = tuple[int, int, int]


def parse_data(puzzle_input: str) -> list[Color]:
    """Parse puzzle input."""
    return [
        (int(r), int(g), int(b))
        for line in puzzle_input.splitlines()
        for r, g, b in [line.split(",")]
    ]


def part1(colors: list[Color]) -> str:
    """Solve part 1."""
    counts = collections.Counter(colors)
    ((most_common, _count),) = counts.most_common(1)
    return ",".join(str(value) for value in most_common)


def part2(colors: list[Color]) -> int:
    """Solve part 2."""
    return sum(label(color) == "Green" for color in colors)


def part3(colors: list[Color]) -> int:
    """Solve part 3."""
    coins = {"Red": 5, "Green": 2, "Blue": 4, "Special": 10}
    return sum(coins[label(color)] for color in colors)


@cache
def label(color: Color):
    """Label one bush color."""
    if len(set(color)) < 3:  # Two or more values are equal
        return "Special"

    values = dict(zip(["Red", "Green", "Blue"], color))
    return max(values, key=lambda lbl: values[lbl])
