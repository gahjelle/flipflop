"""Flip Flop puzzle 8, 2026: The Amazing Digital Stoats."""

import collections
import itertools

type Population = dict[str, int]
type Rules = dict[str, Population]


def parse_data(puzzle_input: str) -> tuple[Rules, Rules]:
    """Parse puzzle input."""
    return parse_single_rules(puzzle_input), parse_double_rules(puzzle_input)


def parse_single_rules(puzzle_input: str) -> Rules:
    """Parse rules for single stoats."""
    stoat_rules = {}
    for line in puzzle_input.splitlines():
        from_stoat, *to_stoats = line.split()
        if from_stoat not in stoat_rules:
            stoat_rules[from_stoat] = to_population("".join(to_stoats))
    return stoat_rules


def parse_double_rules(puzzle_input: str) -> Rules:
    """Parse rules for stoat pairs."""
    stoat_rules = {}
    for line in puzzle_input.splitlines():
        first, second, *to_stoats = line.split()
        stoat_rules[first + second] = to_population_pairs(
            "".join([first, *to_stoats, second])
        )
        stoat_rules[second + first] = to_population_pairs(
            "".join([second, *to_stoats, first])
        )
    return stoat_rules


def part1(data: tuple[Rules, Rules]) -> int:
    """Solve part 1."""
    rules, _ = data
    population = {"A": 1, "B": 1}
    for _ in range(7):
        population = evolve(population, rules=rules)

    return sum(population.values())


def part2(data: tuple[Rules, Rules]) -> int:
    """Solve part 2."""
    _, rules = data
    population = {"AB": 1}
    for _ in range(7):
        population = evolve(population, rules=rules)
    return sum(population.values()) + 1  # #stoats is #pairs plus one


def part3(data: tuple[Rules, Rules]) -> int:
    """Solve part 3."""
    _, rules = data
    population = {"AB": 1}
    for _ in range(21):
        population = evolve(population, rules=rules)
    return sum(population.values()) + 1  # #stoats is #pairs plus one


def to_population(stoats: str) -> Population:
    """Convert a stoats string (AABAC) to a population ({'A': 3, 'B': 1, 'C': 1}).

    Stoats are listed in alphabetical order.

    # Examples

    >>> to_population("AABAC")
    {'A': 3, 'B': 1, 'C': 1}
    """
    population = dict.fromkeys("ABCDEFGHIJ", 0)
    for stoat in stoats:
        population[stoat] += 1
    return {stoat: count for stoat, count in population.items() if count}


def to_population_pairs(stoats: str) -> Population:
    """Convert stoats to a paired population."""
    population = collections.defaultdict(int)
    for first, second in itertools.pairwise(stoats):
        population[first + second] += 1
    return {pair: count for pair, count in population.items() if count}


def evolve(population: Population, rules: Rules) -> Population:
    """Evolve a population one generation."""
    new_population = collections.defaultdict(int)
    for from_stoat, from_count in population.items():
        for to_stoat, to_count in rules[from_stoat].items():
            new_population[to_stoat] += from_count * to_count
    return {stoat: count for stoat, count in new_population.items() if count}
