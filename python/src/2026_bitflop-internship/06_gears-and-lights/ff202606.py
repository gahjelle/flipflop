"""Flip Flop puzzle 6, 2026: Gears and Lights."""

import collections
import string

type Coordinate = tuple[int, int]
type Grid = dict[Coordinate, str]
type Connections = dict[Coordinate, Coordinate]


def parse_data(puzzle_input: str) -> Grid:
    """Parse puzzle input."""
    return {
        (row, col): char
        for row, line in enumerate(puzzle_input.splitlines())
        for col, char in enumerate(line)
    }


def part1(grid: Grid) -> int:
    """Solve part 1."""
    gears = rotate_gears(grid, gears="#")
    lights = sorted(pos for pos, item in grid.items() if item == "*")
    sequence = "".join(classify_light(gears, light) for light in lights)
    return int(sequence, base=2)


def part2(grid: Grid) -> int:
    """Solve part 2."""
    bluetooths = connect_bluetooth(grid)
    gears = rotate_gears(grid, gears="#3", bluetooths=bluetooths)
    lights = sorted(pos for pos, item in grid.items() if item == "*")
    sequence = "".join(classify_light(gears, light) for light in lights)
    return int(sequence, base=2)


def part3(grid: Grid) -> int:
    """Solve part 3."""
    bluetooths = {
        from_pos: to_pos
        for from_pos, to_pos in connect_bluetooth(grid).items()
        if not is_prime(len(find_group(grid, gears="#3", start=to_pos)))
    }
    gears = rotate_gears(grid, gears="#3", bluetooths=bluetooths)
    lights = sorted(pos for pos, item in grid.items() if item == "*")
    sequence = "".join(classify_light(gears, light) for light in lights)
    return int(sequence, base=2)


def _print_grid(grid: Grid) -> None:
    """Print a grid to the console."""
    max_row, max_col = max(grid)
    for row in range(max_row + 1):
        for col in range(max_col + 1):
            print(grid.get((row, col), "."), end="")
        print()


def connect_bluetooth(grid: Grid) -> Connections:
    """Set up bluetooth connections."""
    connections: Connections = {}
    for from_pos, char in grid.items():
        if char not in string.ascii_lowercase:
            continue

        to_pos = next(pos for pos, tc in grid.items() if tc == char.upper())
        connections[from_pos] = to_pos

    return connections


def find_group(grid: Grid, gears: str, start: Coordinate) -> set[Coordinate]:
    """Find gears in a given group."""
    seen: set[Coordinate] = set()
    queue = collections.deque([start])
    while queue:
        pos = queue.popleft()
        seen.add(pos)

        for new_pos in neighbors(pos):
            if new_pos in seen:
                continue
            if grid.get(new_pos, "outside") in gears:
                queue.append(new_pos)

    return seen - {start}


def rotate_gears(grid: Grid, gears: str, bluetooths: Connections | None = None) -> Grid:
    """Find rotation of all gears."""
    gear_grid: Grid = {}
    bluetooths = {} if bluetooths is None else bluetooths
    start = next(pos for pos, char in grid.items() if char == "S")

    seen: set[Coordinate] = set()
    queue = collections.deque([(start, "L")])
    while queue:
        pos, direction = queue.popleft()
        if grid[pos] in gears:
            gear_grid[pos] = direction
        seen.add(pos)

        for new_pos in neighbors(pos):
            if new_pos in seen:
                continue
            if new_pos in bluetooths:
                new_pos = bluetooths[new_pos]
                queue.append((new_pos, direction))
            if grid.get(new_pos, "outside") in gears:
                queue.append((new_pos, "R" if direction == "L" else "L"))
    return gear_grid


def classify_light(grid: Grid, light: Coordinate) -> str:
    """Classify one light as high (1, adj to R) or low (0, adj to L)."""
    rotations = {grid.get(pos) for pos in neighbors(light)}
    return "1" if "R" in rotations else "0" if "L" in rotations else ""


def is_prime(number: int) -> bool:
    """Check if a given number is prime."""
    small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]
    if number in small_primes:
        return True
    if number < small_primes[-1]:
        return False
    for prime in small_primes:
        if number % prime == 0:
            return False
    if number > small_primes[-1] ** 2:
        raise ValueError(f"Could not determine if {number} is prime")
    return True


def neighbors(pos: Coordinate) -> list[Coordinate]:
    """Find neighbors of a given position."""
    row, col = pos
    return [(row - 1, col), (row, col - 1), (row, col + 1), (row + 1, col)]
