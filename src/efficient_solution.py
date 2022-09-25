import time
import argparse
from memory_profiler import memory_usage
from mismatch_cost import mismatch_cost, gap_cost
from str_generator import generate_input_string
from typing import List


def space_efficient_alignment(x: str, y: str) -> List:
    '''
    use linear memory to run the alignment
    transpose the matrix to improve the performance
    opt[j][i] is B[i][j] in the textbook
    '''
    m = len(x)
    n = len(y)
    # allocate 2d array 2 * (m + 1)
    opt = [[0] * (m + 1) for _ in range(0, 2)]
    # init the base case
    for i in range(0, m + 1):
        opt[0][i] = i * gap_cost
    # because the matrix is transposed
    # iterate over j first
    for j in range(1, n + 1):
        char_y = y[j - 1]
        opt[1][0] = j * gap_cost
        for i in range(1, m + 1):
            char_x = x[i - 1]
            opt[1][i] = min(
                min(mismatch_cost[char_x][char_y] + opt[0][i - 1], gap_cost + opt[0][i]),
                gap_cost + opt[1][i - 1]
            )
        # swap two arrays
        tmp = opt[0]
        opt[0] = opt[1]
        opt[1] = tmp
    return opt[0]


def backward_space_efficient_alignment(x: str, y: str) -> int:
    # reverse two string
    rev_x = x[::-1]
    rev_y = y[::-1]
    return space_efficient_alignment(rev_x, rev_y)


def alignment(x: str, x_base_index: int,
              y: str, y_base_index: int,
              path: List) -> int:
    '''
    basic alignment
    for the base case in devide and conquer
    m <=2 or n <= 2 so it also uses linear memory
    '''
    m = len(x)
    n = len(y)
    # allocate 2d array (m + 1) * (n + 1)
    opt = [[0] * (n + 1) for _ in range(0, m + 1)]
    for i in range(1, m + 1):
        opt[i][0] = i * gap_cost
    for j in range(1, n + 1):
        opt[0][j] = j * gap_cost

    for i in range(1, m + 1):
        char_x = x[i - 1]
        for j in range(1, n + 1):
            char_y = y[j - 1]
            opt[i][j] = min(
                min(mismatch_cost[char_x][char_y] + opt[i - 1][j - 1], gap_cost + opt[i - 1][j]),
                gap_cost + opt[i][j - 1]
            )
    path += build_path(opt, x, x_base_index, y, y_base_index)
    return opt[m][n]


def build_path(opt: List[List],
               x: str, x_base_index: int,
               y: str, y_base_index: int) -> List:
    m = len(x)
    n = len(y)
    i = m
    j = n
    path = [(m + x_base_index, n + y_base_index)]
    while (i > 0 and j > 0):
        if (opt[i - 1][j - 1] + mismatch_cost[x[i - 1]][y[j - 1]]) == opt[i][j]:
            i -= 1
            j -= 1
        elif (opt[i - 1][j] + gap_cost) == opt[i][j]:
            i -= 1
        elif (opt[i][j - 1] + gap_cost) == opt[i][j]:
            j -= 1
        path.insert(0, (i + x_base_index, j + y_base_index))
    while (i > 0):
        i -= 1
        path.insert(0, (i + x_base_index, j + y_base_index))
    while (j > 0):
        j -= 1
        path.insert(0, (i + x_base_index, j + y_base_index))
    path.remove((x_base_index, y_base_index))
    return path


def build_alignment_from_path(path: List, x: str, y: str):
    path.sort(key=lambda item: item[0])
    path.sort(key=lambda item: item[1])
    last_step = (0, 0)
    alignment_x = ""
    alignment_y = ""
    for step in path:
        i, j = step
        if i > last_step[0] and j > last_step[1]:
            alignment_x += x[i - 1]
            alignment_y += y[j - 1]
        elif i > last_step[0]:
            alignment_x += x[i - 1]
            alignment_y += '_'
        elif j > last_step[1]:
            alignment_x += '_'
            alignment_y += y[j - 1]
        last_step = step
    return alignment_x, alignment_y


def devide_and_conquer_alignment_helper(x: str, x_base_index: int,
                                        y: str, y_base_index: int,
                                        path: List):
    m = len(x)
    n = len(y)
    # base case
    if m <= 2 or n <= 2:
        alignment(x, x_base_index, y, y_base_index, path)
        return
    left_y = y[:int(n/2)]
    left_y_base_index = y_base_index

    right_y = y[int(n/2):]
    right_y_base_index = y_base_index + int(n/2)
    q = None
    min_path_sum = float("inf")

    opt_left = space_efficient_alignment(x, left_y)
    opt_right = backward_space_efficient_alignment(x, right_y)
    for i in range(0, m + 1):
        path_sum = opt_left[i] + opt_right[m - i]
        if min_path_sum > path_sum:
            q = i
            min_path_sum = path_sum

    split_x = x_base_index + q
    split_y = y_base_index + int(n/2)
    path.append((split_x, split_y))

    devide_and_conquer_alignment_helper(x[:q], x_base_index,
                                        y[:int(n/2)], y_base_index, path)
    devide_and_conquer_alignment_helper(x[q:], x_base_index + q,
                                        y[int(n/2):], y_base_index + int(n/2), path)


def devide_and_conquer_alignment(x: str, y: str):
    path = []
    devide_and_conquer_alignment_helper(x, 0, y, 0, path)
    return build_alignment_from_path(path, x, y)



run_time_in_secs = None
input_x = None
input_y = None
alignment_x = None
alignment_y = None


def run_alignment():
    #  input strings
    global run_time_in_secs, alignment_x, alignment_y, input_x, input_y
    start_time = time.time()
    alignment_x, alignment_y = devide_and_conquer_alignment(input_x, input_y)
    end_time = time.time()
    run_time_in_secs = end_time - start_time


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Align two string (Space-efficient Algorithm)')
    parser.add_argument('input_file', help='Input file name')
    args = parser.parse_args()
    input_x, input_y = generate_input_string(args.input_file)
    mem  = memory_usage(run_alignment)
    memory_in_kbs = max(mem) * 1024
    ans_cost = 0
    for u, v in zip(alignment_x, alignment_y):
        if u == '_' or v == '_':
            ans_cost += gap_cost
        else:
            ans_cost += mismatch_cost[u][v]
    with open('output.txt', 'w') as output:
        output.write('{} {}\n'.format(alignment_x[:50], alignment_x[-50:]))
        output.write('{} {}\n'.format(alignment_y[:50], alignment_y[-50:]))
        output.write('{}\n'.format(ans_cost))
        output.write('{:.4f}\n'.format(run_time_in_secs))
        output.write('{}\n'.format(memory_in_kbs))
