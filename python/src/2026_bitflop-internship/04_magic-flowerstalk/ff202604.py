"""Flip Flop puzzle 4, 2026: Magic Flowerstalk."""

import itertools


def parse_data(puzzle_input: str) -> list[str]:
    """Parse puzzle input."""
    return [("L" if "o-|" in line else "R" if "|-o" in line else "") for line in puzzle_input.splitlines()[::-1]]

def part1(tree: list[str]) -> int:
    """Solve part 1."""
    height = len(tree)
    cut = 400 if height > 400 else 8  # Capture example
    return len("".join(tree[cut+1:]))


def part2(tree: list[str]) -> int:
    """Solve part 2."""
    leaves = "".join(tree)
    return sum(first != second for first, second in itertools.pairwise(leaves))

def part3(tree: list[str]) -> int:
    """Solve part 3."""
    leaves = "".join(tree)
    worker_num = 0
    while any(leaves):
        leaves = "".join([
            first * (first == second)
            for first, second in itertools.pairwise(leaves)
        ])
        worker_num += 1

    return worker_num