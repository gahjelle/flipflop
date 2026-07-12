"""Flip Flop puzzle 7, 2026: Ross's Pet Snake."""

import collections
from typing import cast

type Move = tuple[int, int]
type Coordinate = tuple[int, int]

MOVES = {">": (1, 0), "^": (0, 1), "<": (-1, 0), "v": (0, -1)}


def parse_data(puzzle_input: str) -> tuple[list[Move], list[Coordinate]]:
    """Parse puzzle input."""
    moves, sushis = puzzle_input.split("\n\n")
    return parse_moves(moves), parse_sushis(sushis)


def parse_moves(line: str) -> list[Move]:
    """Parse moves."""
    return [MOVES[move] for move in line]


def parse_sushis(lines: str) -> list[Coordinate]:
    """Parse sushis."""
    return [
        cast("Coordinate", tuple(map(int, line.split(","))))
        for line in lines.splitlines()
    ]


def part1(data: tuple[list[Move], list[Coordinate]]) -> int:
    """Solve part 1."""
    moves, sushis = data
    num_moves = len(moves)
    return get_sushi(moves[: num_moves // 2], sushis)


def part2(data: tuple[list[Move], list[Coordinate]]) -> int:
    """Solve part 2."""
    moves, sushis = data
    return play_snake(moves, sushis)


def part3(data: tuple[list[Move], list[Coordinate]]) -> int:
    """Solve part 3."""
    moves, sushis = data
    length, num_selfeats = play_cannibal_snake(moves, sushis)
    return length * num_selfeats


def get_sushi(moves: list[Move], sushis: list[Coordinate]) -> int:
    """Get sushi with the snake's head."""
    x, y, sushi = 0, 0, 0
    for dx, dy in moves:
        x, y = x + dx, y + dy
        if (x, y) == sushis[sushi]:
            sushi += 1
    return sushi


def play_snake(moves: list[Move], sushis: list[Coordinate]) -> int:
    """Play a game of snake."""
    snake = collections.deque([(0, 0)])
    sushi = 0
    for dx, dy in moves:
        x, y = snake[-1]
        snake.append((x + dx, y + dy))
        if snake[-1] == sushis[sushi]:
            sushi += 1
        else:
            snake.popleft()
        # print(snake)
        if len(set(snake)) < len(snake):
            break
    return len(snake)


def play_cannibal_snake(moves: list[Move], sushis: list[Coordinate]) -> tuple[int, int]:
    """Play a game of cannibal snake, where the snake may eat itself."""
    snake = [(0, 0)]
    sushis = sushis + [(-1, -1)]
    sushi, num_selfeats = 0, 0
    for dx, dy in moves:
        x, y = snake[-1]
        snake.append((x + dx, y + dy))
        if snake[-1] == sushis[sushi]:
            sushi += 1
        else:
            snake = snake[1:]
        if len(set(snake)) < len(snake):
            index = snake.index(snake[-1])
            snake = snake[index + 2 :]
            num_selfeats += 1
    return len(snake), num_selfeats
