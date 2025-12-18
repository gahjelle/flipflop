"""Flip Flop puzzle 1, 2025: Banana Contest."""


def parse_data(puzzle_input: str) -> tuple[list[str], list[int]]:
    """Parse puzzle input."""
    bananas = puzzle_input.splitlines()
    return bananas, [len(banana) // 2 for banana in bananas]


def part1(data: tuple[list[str], list[int]]) -> int:
    """Solve part 1."""
    _, lengths = data
    return sum(lengths)


def part2(data: tuple[list[str], list[int]]) -> int:
    """Solve part 2."""
    _, lengths = data
    return sum(length for length in lengths if length % 2 == 0)


def part3(data: tuple[list[str], list[int]]) -> int:
    """Solve part 3."""
    return sum(length for banana, length in zip(*data) if "ne" not in banana)
