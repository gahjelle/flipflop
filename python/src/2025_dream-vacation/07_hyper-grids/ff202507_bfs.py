"""Flip Flop puzzle 7, 2025: Hyper Grids."""

from functools import cache

type Size = tuple[int, int]


def parse_data(puzzle_input: str) -> list[Size]:
    """Parse puzzle input."""
    return [
        (int(w), int(h))
        for line in puzzle_input.splitlines()
        for w, h in [line.split()]
    ]


def part1(sizes: list[Size]) -> int:
    """Solve part 1."""
    return sum(bfs2d(width, height) for width, height in sizes)


def part2(sizes: list[Size]) -> int:
    """Solve part 2."""
    return sum(bfs3d(width, height, width) for width, height in sizes)


def part3(sizes: list[Size]) -> int:
    """Solve part 3."""
    return sum(bfsnd(*([size] * num_dims)) for num_dims, size in sizes)


@cache
def bfs2d(x: int, y: int) -> int:
    """Find number of shortest paths from (x, y) to the first corner.

    The shortest path always moves up or to the left. This is represented by
    only letting x and y decrease by 1 at each step. (This is reversed compared
    with the puzzle text, but easier to track.)

    Note: Can use bfsnd() for this with n=2 dimensions, but this dedicated
    function is faster.

    ## Example

    >>> bfs2d(4, 7)
    84
    """
    if x == 1 and y == 1:
        return 1

    return (bfs2d(x - 1, y) if x > 1 else 0) + (bfs2d(x, y - 1) if y > 1 else 0)


@cache
def bfs3d(x: int, y: int, z: int) -> int:
    """Find number of shortest paths from (x, y, z) to the first corner."""
    if x == 1 and y == 1 and z == 1:
        return 1

    return (
        (bfs3d(x - 1, y, z) if x > 1 else 0)
        + (bfs3d(x, y - 1, z) if y > 1 else 0)
        + (bfs3d(x, y, z - 1) if z > 1 else 0)
    )


@cache
def bfsnd(*xs: int) -> int:
    """Find the number of shortest paths from (x1, x2, ...) to the first corner."""
    if all(x == 1 for x in xs):
        return 1
    return sum(
        bfsnd(*[*xs[:idx], x - 1, *xs[idx + 1 :]]) if x > 1 else 0
        for idx, x in enumerate(xs)
    )
