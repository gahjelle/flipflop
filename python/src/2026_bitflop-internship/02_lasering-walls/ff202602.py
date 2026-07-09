"""Flip Flop puzzle 2, 2026: Lasering Walls."""


def parse_data(puzzle_input: str) -> list[int]:
    """Parse puzzle input."""
    return [{"<": -1, ">": 1}[char] for char in puzzle_input]


def part1(data: list[int]) -> int:
    """Solve part 1."""
    heat = {n: 0 for n in range(1, 101)}
    current = 1
    for move in data:
        current = in_range(current + move)
        heat[current] += 1

    segment, temp = max(heat.items(), key=warmest)
    return segment * temp


def part2(data: list[int]) -> int:
    """Solve part 2."""
    heat = 0
    robot, wall = 1, 1
    for r_move, w_move in zip(data, data[::-1], strict=True):
        robot, wall = in_range(robot + r_move), in_range(wall + w_move)
        heat += robot == wall
    return heat


def part3(data: list[int]) -> int:
    """Solve part 3."""
    heat = {n: 0 for n in range(1, 101)}
    current = 1
    for r_move, w_move in zip(data, data[::-1], strict=True):
        current = in_range(current + r_move - w_move)
        heat[current] += 1

    segment, temp = max(heat.items(), key=warmest)
    return segment * temp


def in_range(number, min=1, max=100) -> int:
    """Keep the number in range, with rollover.

    # Examples:

    >>> in_range(42)
    42
    >>> in_range(0)
    100
    >>> in_range(101)
    1
    >>> in_range(-3)
    97
    """
    return (
        max - (min - number) + 1
        if number < min
        else min + (number - max) - 1
        if number > max
        else number
    )


def warmest(item: tuple[int, int]) -> tuple[int, int]:
    """Classify the warmest segment, break ties by segment number."""
    segment, temperature = item
    return temperature, -segment
