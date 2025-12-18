"""Flip Flop puzzle 6, 2025: Bird Spotters."""

type Coordinate = tuple[int, int]


def parse_data(puzzle_input: str) -> list[Coordinate]:
    """Parse puzzle input."""
    return [
        (int(x), int(y))
        for line in puzzle_input.splitlines()
        for x, y in [line.split(",")]
    ]


def part1(speeds: list[Coordinate]) -> int:
    """Solve part 1."""
    size = 1000 if len(speeds) > 20 else 8
    positions = move(
        num_ticks=100, speeds=speeds, positions=[(0, 0)] * len(speeds), size=size
    )
    return in_frame(positions, size=size)


def part2(speeds: list[Coordinate]) -> int:
    """Solve part 2."""
    size = 1000 if len(speeds) > 20 else 8
    positions = [(0, 0)] * len(speeds)
    speeds_per_hour = move(
        num_ticks=3600, speeds=speeds, positions=positions, size=size
    )

    num_birds = 0
    for _ in range(1000):
        positions = tick(speeds=speeds_per_hour, positions=positions, size=size)
        num_birds += in_frame(positions, size=size)
    return num_birds


def part3(speeds: list[Coordinate]) -> int:
    """Solve part 3."""
    size = 1000 if len(speeds) > 20 else 8
    positions = [(0, 0)] * len(speeds)
    speeds_per_year = move(
        num_ticks=31_556_926, speeds=speeds, positions=positions, size=size
    )

    num_birds = 0
    for _ in range(1000):
        positions = tick(speeds=speeds_per_year, positions=positions, size=size)
        num_birds += in_frame(positions, size=size)
    return num_birds


def tick(
    speeds: list[Coordinate], positions: list[Coordinate], size: int
) -> list[Coordinate]:
    """Move one tick based on the speeds."""
    return [
        ((x + dx) % size, (y + dy) % size)
        for (x, y), (dx, dy) in zip(positions, speeds)
    ]


def move(
    num_ticks: int,
    speeds: list[Coordinate],
    positions: list[Coordinate],
    size: int,
) -> list[Coordinate]:
    """Move several ticks."""
    if num_ticks == 0:
        return positions
    if num_ticks == 1:
        return tick(speeds, positions, size)

    double, rest = divmod(num_ticks, 2)
    positions = [
        (2 * x % size, 2 * y % size) for x, y in move(double, speeds, positions, size)
    ]
    return tick(speeds, positions, size) if rest else positions


def in_frame(positions: list[Coordinate], size: int) -> int:
    """Count the number of birds in frame."""
    min_frame, max_frame = size // 4, size // 4 * 3
    return sum(
        min_frame <= x < max_frame and min_frame <= y < max_frame for x, y in positions
    )
