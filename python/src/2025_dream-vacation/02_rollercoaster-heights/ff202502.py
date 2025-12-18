"""Flip Flop puzzle 2, 2025: Rollercoaster Heights."""

import itertools
from functools import cache


def parse_data(puzzle_input: str) -> list[int]:
    """Parse puzzle input."""
    moves = {"^": 1, "v": -1}
    return [moves[char] for char in puzzle_input]


def part1(moves: list[int]) -> int:
    """Solve part 1."""
    return max_accumulated(moves)


def part2(moves: list[int]) -> int:
    """Solve part 2."""
    count, acc_moves = 0, []
    for previous, current in itertools.pairwise([0, *moves]):
        if current != previous:
            count = 0
        count += 1
        acc_moves.append(count * current)
    return max_accumulated(acc_moves)


def part3(moves: list[int]) -> int:
    """Solve part 3."""
    count, acc_moves = 0, []
    for previous, current in itertools.pairwise([0, *moves, 0]):
        if current != previous:
            acc_moves.append(fib(count) * previous)
            count = 0
        count += 1
    return max_accumulated(acc_moves)


def max_accumulated(moves: list[int]) -> int:
    """Find the maximum of the accumulated values.

    ## Examples

    >>> max_accumulated([1, 2, 3, -4, 2])
    6
    >>> max_accumulated([-10, 1, 2, 3, 2])
    0
    >>> max_accumulated([1, 2, 3, 4])
    10
    """
    return max(itertools.accumulate([0, *moves]))


@cache
def fib(number):
    """Calculate Fibonacci numbers.

    ## Examples

    >>> fib(0)
    0
    >>> fib(1)
    1
    >>> fib(2)
    1
    >>> fib(10)
    55
    """
    return number if number <= 1 else fib(number - 1) + fib(number - 2)
