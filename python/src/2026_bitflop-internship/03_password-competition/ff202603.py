"""Flip Flop puzzle 3, 2026: Password Competition."""

import string


def parse_data(puzzle_input: str) -> list[str]:
    """Parse puzzle input."""
    return puzzle_input.splitlines()


def part1(data: list[str]) -> str:
    """Solve part 1."""
    rules = [has_lower, has_upper, has_digit]
    scores = {password: calculate(password, rules=rules) for password in data}
    return max(scores, key=lambda password: scores[password])


def part2(data: list[str]) -> str:
    """Solve part 2."""
    rules = [has_lower, has_upper, has_digit, contains_only_seven, longest_sequence]
    scores = {
        password: calculate(password, rules=rules, multiply=contains_color)
        for password in data
    }
    return max(scores, key=lambda password: scores[password])


def part3(data: list[str]) -> int:
    """Solve part 3."""
    rules = [has_lower, has_upper, has_digit, contains_only_seven, longest_sequence]
    return max(
        sum(
            calculate(password + suffix, rules=rules, multiply=contains_color)
            for password in data
        )
        for suffix in string.ascii_letters + string.digits
    )


def calculate(password: str, rules: list, multiply=None) -> int:
    """Calculate the score of a password."""
    score = sum(rule(password) for rule in rules)
    multiplier = 1 if multiply is None else multiply(password)
    return score * multiplier * len(password)


def has_lower(password: str) -> bool:
    """Check if password has a lowercase character."""
    return any(char in string.ascii_lowercase for char in password)


def has_upper(password: str) -> bool:
    """Check if password has an uppercase character."""
    return any(char in string.ascii_uppercase for char in password)


def has_digit(password: str) -> bool:
    """Check if password has a digit character."""
    return any(char in string.digits for char in password)


def contains_only_seven(password: str) -> int:
    """Add 7 points for containing 7 and no other digits."""
    return 7 if (set(password) & set(string.digits) == {"7"}) else 0


def longest_sequence(password: str) -> int:
    """Score n^2 for the longest sequence of identical characters."""
    identical = password
    longest = 0
    while any(identical):
        identical = [
            (curr == prev) * curr
            for prev, curr in zip(identical[:-1], identical[1:], strict=True)
        ]
        longest += 1
    if longest < 3:
        return 0
    return longest**2


def contains_color(password: str) -> int:
    """Multiply by 3 if any color: red, green, blue appears in the password"""
    return 3 if any(color in password for color in ["red", "green", "blue"]) else 1
