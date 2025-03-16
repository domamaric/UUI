import ctypes
import timeit
import cProfile
import pprint

import re

# Load the shared library
file_reader_lib = ctypes.CDLL('./libparse.so')


def read_space_state_regex(filepath="3x3_puzzle.txt"):
    with open(filepath, "r") as f:
        lines = f.readlines()

    # Remove comment lines and strip spaces
    lines = [line.strip() for line in lines if not re.match(r'^\s*#', line) and line.strip()]

    initial_state = lines[0] if lines else None
    target_states = lines[1].split() if len(lines) > 1 else []

    state_transitions = {}

    # Regex pattern for parsing transitions
    pattern = re.compile(r"(\w+):\s*((?:\w+,\d+\s*)*)")  

    for line in lines[2:]:  # Skip first two lines
        match = pattern.match(line)
        if match:
            state = match.group(1)
            transitions_text = match.group(2)

            # Extract (successor, cost) pairs using another regex
            transitions = re.findall(r"(\w+),(\d+)", transitions_text)
            state_transitions[state] = [(s, int(c)) for s, c in transitions]

    return {
        "initial_state": initial_state,
        "target_states": target_states,
        "transitions": state_transitions,
    }


def read_space_state():

    def remove_comments(file_lines):
        removed_comments = []

        for line in file_lines:
            if not line.startswith('#'):
                removed_comments.append(line.strip())

        return removed_comments
    
    successor_dict = {}
    initial_state = None
    target_states = []
    path = "3x3_puzzle.txt"

    with open(path, 'r') as f:
        file_lines = remove_comments([x for x in f.readlines()])

        initial_state = file_lines[0]
        target_states = file_lines[1].split()

        for line in file_lines[2:]:
            state, successors = line.split(':')
            state = state.strip()
            successors = successors.strip().split()
            successor_list = []

            for successor in successors:
                next_state, cost = successor.split(',')
                successor_list.append((next_state, float(cost)))
            successor_dict[state] = successor_list

    return successor_dict, initial_state, target_states


def read_file(filename="3x3_puzzle.txt"):
    lines_dict = {}

    # Define the C callback function directly
    @ctypes.CFUNCTYPE(None, ctypes.c_char_p, ctypes.c_char_p)
    def c_line_callback(key, values):
        # Decode once and store
        lines_dict[key.decode('utf-8')] = values.decode('utf-8')

    c_filename = ctypes.c_char_p(filename.encode('utf-8'))

    # Call the C function with the optimized callback
    file_reader_lib.read_file_line_by_line(c_filename, c_line_callback)

    with open(filename, 'r') as f:
        file_lines = f.readlines(33)  # Read first 33 bytes, assuming that's intended
        initial_state = file_lines[0].strip()
        target_states = file_lines[1].split()

    return lines_dict, initial_state, target_states


if __name__ == "__main__":
    # print(timeit.timeit("read_file()", setup="from __main__ import read_file", number=1))
    # print(timeit.timeit("read_space_state()", setup="from __main__ import read_space_state", number=1))

    # result_dict = read_file()
    # breakpoint()
    # pprint.pprint(result_dict)

    cProfile.run('read_file()')
    # cProfile.run('read_space_state()')
    # cProfile.run('read_space_state_regex()')
    # result_dict, _, _ = read_space_state()
    # pprint.pprint(result_dict)