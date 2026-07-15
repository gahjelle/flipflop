"""Flip Flop puzzle 9, 2026: Thinking With Mazes."""

import collections

type Coordinate = tuple[int, int]
type Direction = tuple[int, int]
type Maze = set[Coordinate]


def parse_data(puzzle_input: str) -> tuple[Maze, Coordinate, Coordinate]:
    """Parse puzzle input."""
    grid = {
        (row, col): char
        for row, line in enumerate(puzzle_input.splitlines())
        for col, char in enumerate(line)
    }
    start = next(pos for pos, char in grid.items() if char == "S")
    end = next(pos for pos, char in grid.items() if char == "E")
    maze = {pos for pos, char in grid.items() if char in "S.E"}
    return maze, start, end


def part1(data: tuple[Maze, Coordinate, Coordinate]) -> int:
    """Solve part 1."""
    maze, start, end = data
    return len(walk_maze(maze, start=start, end=end))


def part2(data: tuple[Maze, Coordinate, Coordinate]) -> int:
    """Solve part 2."""
    maze, start, end = data
    return len(walk_maze(maze, start=start, end=end, use_teleport=True))


def part3(data: tuple[Maze, Coordinate, Coordinate]) -> int:
    """Solve part 3."""
    maze, start, end = data
    return walk_maze_w_portal_gun(maze, start=start, end=end)


def walk_maze(
    maze: Maze,
    start: Coordinate,
    end: Coordinate,
    *,
    use_teleport: bool = False,
) -> list[Coordinate]:
    """Walk the maze from start to end, find the shortest path."""
    queue = collections.deque([(start, [])])
    seen: set[Coordinate] = set()
    while queue:
        (row, col), path = queue.popleft()
        if (row, col) == end:
            return path
        if (row, col) in seen:
            continue
        seen.add((row, col))

        for npos in steps(maze, row, col, use_teleport=use_teleport):
            queue.append((npos, [*path, npos]))
    return []


def steps(
    maze: Maze,
    row: int,
    col: int,
    *,
    use_single: bool = True,
    use_teleport: bool = False,
) -> set[Coordinate]:
    """Find the possible steps in the maze."""
    directions = [(-1, 0), (0, -1), (0, 1), (1, 0)]
    single_steps = (
        {(row + dr, col + dc) for dr, dc in directions} if use_single else set()
    )
    if not use_teleport:
        return single_steps & maze
    portal_steps = {teleport(maze, row, col, dr, dc) for dr, dc in directions}
    return (single_steps | portal_steps) & maze


def teleport(maze: Maze, row: int, col: int, drow: int, dcol: int) -> Coordinate:
    """Calculate target (end of hall) for teleporting in each direction."""
    while True:
        if (row + drow, col + dcol) not in maze:
            return row, col
        row, col = row + drow, col + dcol


def walk_maze_w_portal_gun(maze: Maze, start: Coordinate, end: Coordinate) -> int:
    """Find the shortest path through the maze using a portal gun."""
    distances = enumerate_maze(maze, start=end)
    queue = collections.deque([(start, 0, (-1, -1), (-1, -1))])
    seen: set[tuple[Coordinate, Coordinate, Coordinate]] = set()
    best_distance = distances[start]
    while queue:
        (row, col), num_steps, portal_a, portal_b = queue.popleft()
        if (row, col) == end:
            return num_steps
        if key((row, col), portal_a, portal_b) in seen:
            continue
        seen.add(key((row, col), portal_a, portal_b))

        # Only consider moves that improve, but buffer with +1 to allow portal
        # gun instead of single step
        if distances[row, col] > best_distance + 1:
            continue
        best_distance = min(best_distance, distances[row, col])

        # Move through portals
        if (row, col) == portal_a and portal_b in maze:
            queue.append((portal_b, num_steps + 1, (-1, -1), portal_b))
        if (row, col) == portal_b and portal_a in maze:
            queue.append((portal_a, num_steps + 1, portal_a, (-1, -1)))

        # Create portals
        for ppos in steps(maze, row, col, use_single=False, use_teleport=True):
            if ppos == portal_a or ppos == portal_b:
                continue
            queue.append(((row, col), num_steps + 1, ppos, portal_b))
            queue.append(((row, col), num_steps + 1, portal_a, ppos))

        # Single steps
        for npos in steps(maze, row, col):
            queue.append((npos, num_steps + 1, portal_a, portal_b))
    return -1


def key(
    pos: Coordinate, portal_a: Coordinate, portal_b: Coordinate
) -> tuple[Coordinate, Coordinate, Coordinate]:
    """Create a key for position and portals encoding symmetry."""
    if portal_a < portal_b:
        return pos, portal_a, portal_b
    else:
        return pos, portal_b, portal_a


def enumerate_maze(maze: Maze, start: Coordinate) -> dict[Coordinate, int]:
    """Enumerate steps inside the maze to calculate distances."""
    distances: dict[Coordinate, int] = {}
    queue = collections.deque([(start, 0)])
    seen: set[Coordinate] = set()
    while queue:
        (row, col), num_steps = queue.popleft()
        if (row, col) in seen:
            continue
        seen.add((row, col))
        distances[row, col] = num_steps

        for npos in steps(maze, row, col):
            queue.append((npos, num_steps + 1))

    return distances
