"""Flip Flop puzzle 3, 2026: Password Competition."""

import itertools
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
    """Check if password has a lowercase character.

    # Examples

    >>> has_lower("abcABC")
    True
    >>> has_lower("ABC123")
    False
    """
    return any(char in string.ascii_lowercase for char in password)


def has_upper(password: str) -> bool:
    """Check if password has an uppercase character.

    # Examples

    >>> has_upper("abcABC")
    True
    >>> has_upper("abc123")
    False
    """
    return any(char in string.ascii_uppercase for char in password)


def has_digit(password: str) -> bool:
    """Check if password has a digit character.

    # Examples

    >>> has_digit("ABC123")
    True
    >>> has_digit("abcABC")
    False
    """
    return any(char in string.digits for char in password)


def contains_only_seven(password: str) -> int:
    """Add 7 points for containing 7 and no other digits.

    Examples:

    >>> contains_only_seven("abc7ABC")
    7
    >>> contains_only_seven("7a7b7c7")
    7
    >>> contains_only_seven("abc")
    0
    >>> contains_only_seven("123456789")
    0
    """
    return 7 if (set(password) & set(string.digits) == {"7"}) else 0


def longest_sequence(password: str) -> int:
    """Score n^2 for the longest sequence of identical characters (> 2).

    # Examples:

    >>> longest_sequence("abcdef")
    0
    >>> longest_sequence("aabcde")
    0
    >>> longest_sequence("abcccd")
    9
    >>> longest_sequence("abbbbc")
    16
    >>> longest_sequence("aaaaab")
    25
    >>> longest_sequence("aaaaaa")
    36
    """
    identical = password
    longest = 0
    while any(identical):
        identical = [
            (curr == prev) * curr for prev, curr in itertools.pairwise(identical)
        ]
        longest += 1
    return 0 if longest < 3 else longest**2


def contains_color(password: str) -> int:
    """Multiply by 3 if any color: red, green, blue appears in the password

    # Examples:

    >>> contains_color("aredbc")
    3
    >>> contains_color("greenblue")
    3
    >>> contains_color("regreeblu")
    1
    """
    return 3 if any(color in password for color in ["red", "green", "blue"]) else 1
