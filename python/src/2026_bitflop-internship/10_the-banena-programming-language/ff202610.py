"""Flip Flop puzzle 10, 2026: The Banena™ Programming Language."""

type State = dict[int, int]
type Instruction = tuple[int, list[int]]
type Instructions = list[Instruction]
type Label = tuple[int, int]
type Labels = dict[int, int]
type Program = tuple[Instructions, Labels]


def parse_data(puzzle_input: str) -> Program:
    """Parse puzzle input."""
    instructions, labels, line_num = [], [], 0
    for line in puzzle_input.splitlines():
        if line.startswith("ba"):
            instructions.append(parse_instruction(line))
            line_num += 1
        if line.startswith("be"):
            labels.append(parse_label(line, index=line_num))
    return instructions, dict(labels)


def parse_instruction(line: str) -> Instruction:
    """Parse one instruction line."""
    instruction, *args = [
        part.count("na") for part in line.removeprefix("ba").split("ne")
    ]
    return instruction, list(args)


def parse_label(line: str, index: int) -> Label:
    """Parse one label line."""
    label_id = line.removeprefix("be").count("na")
    return label_id, index


def part1(program: Program) -> int:
    """Solve part 1."""
    state, _ = execute_program(program)
    return state[0]


def part2(program: Program) -> int:
    """Solve part 2.

    Use that there is a mod 16 in the program causing the halting pattern to
    repeat for every 16th r0-value.
    """
    max_num_instructions = 5_000_000
    first_16 = [
        counts
        for r0 in range(16)
        for _, counts in [
            execute_program(program, r0=r0, max_num_instructions=max_num_instructions)
        ]
    ]
    all = (first_16 * 7)[:100]
    return sum(counts >= max_num_instructions for counts in all)


def part3(program: Program) -> int:
    """Solve part 3.

    Use that there is a mod 16 in the program causing the halting pattern to
    repeat for every 16th r0-value.
    """
    total_count = 0
    max_num_instructions = 5_000_000
    for r1 in range(16):
        first_16 = sum(
            counts >= max_num_instructions
            for r0 in range(16)
            for _, counts in [
                execute_program(
                    program, r0=r0, r1=r1, max_num_instructions=max_num_instructions
                )
            ]
        )
        total_count += first_16 * (65536 // 16)
    return total_count


def execute_program(
    program: Program, r0: int = 0, r1: int = 0, max_num_instructions: int = 5_000_000
) -> tuple[State, int]:
    """Execute one program."""
    instructions, labels = program
    current, count = 0, 0
    state = {reg: 0 for reg in range(16)} | {0: r0, 1: r1}
    while current < len(instructions):
        state, to_label = execute_instruction(state, instructions[current])
        if to_label is None:
            current += 1
        else:
            current = labels[to_label]
        count += 1
        if count >= max_num_instructions:
            break
    return state, count


def execute_instruction(
    state: State, instruction: Instruction
) -> tuple[State, int | None]:
    """Execute one instruction."""
    match instruction:
        case 0, [value, destination]:
            return state | {destination: value}, None
        case 1, [source, destination]:
            return state | {destination: state[source]}, None
        case 2, [first, second, destination]:
            return state | {destination: uint(state[first] + state[second])}, None
        case 3, [first, second, destination]:
            return state | {destination: uint(state[first] - state[second])}, None
        case 4, [first, second, destination]:
            return state | {destination: uint(state[first] * state[second])}, None
        case 5, [first, second, destination]:
            if state[second] == 0:
                return state | {destination: 0}, None
            return state | {destination: uint(state[first] % state[second])}, None
        case 6, [destination]:
            return state | {destination: uint(state[destination] + 1)}, None
        case 7, [destination]:
            return state | {destination: uint(state[destination] - 1)}, None
        case 8, [label]:
            return state, label
        case 9, [source, label]:
            if state[source] == 0:
                return state, label
            return state, None
        case 10, [source, label]:
            if state[source] != 0:
                return state, label
            return state, None
        case _:
            print(f"Unhandled: {instruction}")
            return state, None


def uint(number: int) -> int:
    """Clamp number to unsigned 16-bit integer."""
    return number % 65536
