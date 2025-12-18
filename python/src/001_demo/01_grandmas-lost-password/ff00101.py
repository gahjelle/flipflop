"""Flip-Flop Demo Puzzle, 2025: Grandma's Lost Password."""

import collections


def parse_data(puzzle_input: str) -> list[int]:
    """Parse puzzle input."""
    return [int(number) for number in puzzle_input.splitlines()]


def part1(numbers: list[int]) -> int:
    """Solve part 1."""
    return sum(numbers)


def part2(numbers: list[int]) -> int:
    """Solve part 2."""
    return round(sum(numbers) / len(numbers))


def part3(numbers: list[int]) -> int:
    """Solve part 3."""
    digit_counts = collections.Counter("".join(str(number) for number in numbers))
    number_counts = collections.Counter(numbers)

    # Find least common digit and most common number
    lc_digit, _ = digit_counts.most_common()[-1]
    mc_number, _ = number_counts.most_common()[0]
    return mc_number * 10 + int(lc_digit)
