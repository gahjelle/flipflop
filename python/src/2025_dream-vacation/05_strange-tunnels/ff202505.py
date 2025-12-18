"""Flip Flop puzzle 5, 2025: Strange Tunnels."""

import collections
from dataclasses import dataclass


@dataclass
class Tunnel:
    """Represent a tunnel."""

    name: str
    start: int
    end: int
    length: int

    @property
    def is_powered(self) -> bool:
        """Check if a tunnel is powered, i.e. has an upper-case name."""
        return self.name.isupper()

    @property
    def powered_steps(self) -> int:
        """When powered, steps are negative."""
        return -self.length if self.is_powered else self.length


def parse_data(puzzle_input: str) -> dict[int, Tunnel]:
    """Parse puzzle input."""
    idxs = collections.defaultdict(list)
    for idx, name in enumerate(puzzle_input):
        idxs[name].append(idx)

    tunnels = {}
    for name, (first, second) in idxs.items():
        tunnels[first] = Tunnel(name, first, second, abs(second - first))
        tunnels[second] = Tunnel(name, second, first, abs(second - first))

    return tunnels


def part1(tunnels: dict[int, Tunnel]) -> int:
    """Solve part 1."""
    current, num_steps = 0, 0
    while current in tunnels:
        num_steps += tunnels[current].length
        current = tunnels[current].end + 1
    return num_steps


def part2(tunnels: dict[int, Tunnel]) -> str:
    """Solve part 2."""
    current, visited = 0, set()
    while current in tunnels:
        visited.add(tunnels[current].name)
        current = tunnels[current].end + 1

    # Use a dict to keep an ordered sequence of unique names
    names = {tunnel.name: 0 for tunnel in tunnels.values()}
    return "".join(name for name in names if name not in visited)


def part3(tunnels: dict[int, Tunnel]) -> int:
    """Solve part 3."""
    current, num_steps = 0, 0
    while current in tunnels:
        num_steps += tunnels[current].powered_steps
        current = tunnels[current].end + 1
    return num_steps
