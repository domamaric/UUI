import ctypes
import timeit
import cProfile
import pprint

# Load the shared library
file_reader_lib = ctypes.CDLL('./libread.so')

# Define the C function signature


def read_space_state():
    successor_dict = {}
    initial_state = None
    target_states = []
    path = "istra.txt"

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


def remove_comments(file_lines):
    removed_comments = []

    for line in file_lines:
        if not line.startswith('#'):
            removed_comments.append(line.strip())

    return removed_comments


def read_file():
    lines_dict = {}  # Dictionary to store lines
    filename = "3x3_puzzle.txt"

    # Define the Python callback function
    def line_callback(key, values):
        # values is type of string
        lines_dict[key] = values.split()

    # Convert the filename to a C-style string
    c_filename = ctypes.c_char_p(filename.encode('utf-8'))

    # Define the C callback function
    @ctypes.CFUNCTYPE(None, ctypes.c_char_p, ctypes.c_char_p)
    def c_line_callback(key, values):
        line_callback(key.decode('utf-8'), values.decode('utf-8'))

    # Call the C function with the C callback
    file_reader_lib.read_file_line_by_line(c_filename, c_line_callback)

    return lines_dict


# Example usage
if __name__ == "__main__":
    # print(timeit.timeit("read_file()",
    #       setup="from __main__ import read_file", number=1))
    # print(timeit.timeit("read_space_state()",
    #       setup="from __main__ import read_space_state", number=1))
    result_dict = read_file()
    # pprint.pprint(result_dict)

    # cProfile.run('read_file()')
    # cProfile.run('read_space_state()')
    # result_dict, _, _ = read_space_state()
    # pprint.pprint(result_dict)
