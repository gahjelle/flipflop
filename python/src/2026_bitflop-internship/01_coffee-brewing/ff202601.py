"""Flip Flop puzzle 1, 2026: Coffee Brewing."""


def parse_data(puzzle_input: str) -> list[int]:
    """Parse puzzle input."""
    return [int(line) for line in puzzle_input.splitlines()]


def part1(data: list[int]) -> int:
    """Solve part 1."""
    return sum(heat_cup(temp) for temp in data)


def part2(data: list[int]) -> int:
    """Solve part 2."""
    return sum(heat_cup(temp) + cool_cup(temp) for temp in data)


def part3(data: list[int]) -> int:
    """Solve part 3."""
    num_cups = len(data) // 2
    temps, prefs = data[:num_cups], data[num_cups:]
    return sum(
        heat_cup(temp, pref) + cool_cup(temp, pref)
        for temp, pref in zip(temps, prefs, strict=True)
    )


def heat_cup(temp: int, preferred: int = 60) -> int:
    """How many seconds does it take to heat up a cup."""
    return preferred - temp if temp < preferred else 0


def cool_cup(temp: int, preferred: int = 60) -> int:
    """How many seconds does it take to cool down a cup."""
    return 5 * (temp - preferred) if temp > preferred else 0
