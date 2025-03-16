import ctypes
import cProfile
import timeit

# Load the shared library
file_parser_lib = ctypes.CDLL('./libparse.so')

StateCallback = ctypes.CFUNCTYPE(None, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int)

file_parser_lib.read_file_line_by_line.argtypes = [ctypes.c_char_p, StateCallback]

def read_file():
    state_space = {}

    def state_callback(state, next_state, cost):
        state = state.decode("utf-8")
        next_state = next_state.decode("utf-8")

        if state not in state_space:
            state_space[state] = []

        state_space[state].append((next_state, cost))

    c_callback = StateCallback(state_callback)

    filename = "3x3_puzzle.txt"
    c_filename = ctypes.c_char_p(filename.encode("utf-8"))

    file_parser_lib.read_file_line_by_line(c_filename, c_callback)

    return state_space

if __name__ == "__main__":
    # print(timeit.timeit("read_file()", setup="from __main__ import read_file", number=1))
    cProfile.run('read_file()')