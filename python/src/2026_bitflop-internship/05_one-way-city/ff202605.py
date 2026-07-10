"""Flip Flop puzzle 5, 2026: One Way City."""

from collections.abc import Callable

type Coordinate = tuple[int, int]
type Direction = tuple[int, int]
type Map = dict[Coordinate, Direction]

DIRECTION = {"^": (-1, 0), "<": (0, -1), ">": (0, 1), "v": (1, 0)}


def parse_data(puzzle_input: str) -> Map:
    """Parse puzzle input."""
    return {
        (row, col): DIRECTION[char]
        for row, line in enumerate(puzzle_input.splitlines())
        for col, char in enumerate(line)
    }


def part1(grid: Map) -> int:
    """Solve part 1."""
    return len(drive(grid, start=(0, 0)))


def part2(grid: Map) -> int:
    """Solve part 2."""
    return len(change_grid(grid, drive, start=(0, 0)))


def part3(grid: Map) -> int:
    """Solve part 3."""
    return len(change_grid(grid, illegal_drive, start=(0, 0)))


def change_grid(
    grid: Map,
    drive_func: Callable[[Map, Coordinate], list[Coordinate]],
    start: Coordinate = (0, 0),
) -> list[Coordinate]:
    """Find the longest drive after changing one street in the grid."""
    streets = drive_func(grid, start)
    longest = streets
    for row, col in streets:
        if any(
            street not in grid
            for street in [
                (row - 1, col),
                (row, col - 1),
                (row, col + 1),
                (row + 1, col),
            ]
        ):
            continue
        for dir in DIRECTION.values():
            if grid[row, col] == dir:
                continue
            new_drive = drive_func(grid | {(row, col): dir}, (0, 0))
            longest = max(longest, new_drive, key=len)
    return longest


def drive(grid: Map, start: Coordinate = (0, 0)) -> list[Coordinate]:
    """Drive a map until you reach an already driven street."""
    (row, col), driven = start, []
    while (row, col) not in driven:
        driven.append((row, col))
        drow, dcol = grid[row, col]
        row, col = row + drow, col + dcol
    return driven


def illegal_drive(grid: Map, start: Coordinate = (0, 0)) -> list[Coordinate]:
    """Drive a map, making three illegal right turns."""
    right_turn = {
        DIRECTION["^"]: DIRECTION[">"],
        DIRECTION[">"]: DIRECTION["v"],
        DIRECTION["v"]: DIRECTION["<"],
        DIRECTION["<"]: DIRECTION["^"],
    }
    (row, col), driven = start, []
    for _ in range(3):
        while (row, col) not in driven:
            driven.append((row, col))
            drow, dcol = grid[row, col]
            row, col = row + drow, col + dcol

        # Make an illegal right turn
        drow, dcol = right_turn[grid[row, col]]
        row, col = row + drow, col + dcol
    return driven
