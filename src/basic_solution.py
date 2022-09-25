import time
import sys
import argparse
from memory_profiler import memory_usage, profile
from mismatch_cost import mismatch_cost, gap_cost
from str_generator import generate_input_string
from typing import List, Tuple


def alignment(x: str, y: str) -> Tuple[int, str, str]:
    m = len(x)
    n = len(y)
    # allocate 2d array (m + 1) * (n + 1)
    opt = [[0] * (n + 1) for _ in range(0, m + 1)]
    # base case
    for i in range(1, m + 1):
        opt[i][0] = i * gap_cost
    for j in range(1, n + 1):
        opt[0][j] = j * gap_cost
    # start DP
    for i in range(1, m + 1):
        char_x = x[i - 1]
        for j in range(1, n + 1):
            char_y = y[j - 1]
            opt[i][j] = min(
                min(mismatch_cost[char_x][char_y] + opt[i - 1][j - 1], gap_cost + opt[i - 1][j]),
                gap_cost + opt[i][j - 1]
            )
    # return min alignment cost and the alignments
    alignment_x, alignment_y = build_alignment_from_opt(opt, x, y)
    return opt[m][n], alignment_x, alignment_y


def build_alignment_from_opt(opt: List[List], x: str, y: str) -> Tuple[str, str]:
    m = len(x)
    n = len(y)
    alignment_x = ""
    alignment_y = ""
    i = m
    j = n
    while (i > 0 and j > 0):
        if (opt[i - 1][j - 1] + mismatch_cost[x[i - 1]][y[j - 1]]) == opt[i][j]:
            alignment_x = x[i - 1] + alignment_x
            alignment_y = y[j - 1] + alignment_y
            i -= 1
            j -= 1
        elif (opt[i - 1][j] + gap_cost) == opt[i][j]:
            alignment_x = x[i - 1] + alignment_x
            alignment_y = '_' + alignment_y
            i -= 1
        elif (opt[i][j - 1] + gap_cost) == opt[i][j]:
            alignment_x = '_' + alignment_x
            alignment_y = y[j - 1] + alignment_y
            j -= 1
    while (i > 0):
        alignment_x = x[i - 1] + alignment_x
        alignment_y = '_' + alignment_y
        i -= 1
    while (j > 0):
        alignment_x = '_' + alignment_x
        alignment_y = y[j - 1] + alignment_y
        j -= 1
    return alignment_x, alignment_y


def build_alignment_from_path(path: List, x: str, y: str) -> Tuple[str, str]:
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


run_time_in_secs = None
min_cost = None
input_x = None
input_y = None
alignment_x = None
alignment_y = None

def run_alignment():
    #  input strings
    global run_time_in_secs, min_cost, alignment_x, alignment_y, input_x, input_y
    start_time = time.time()
    min_cost, alignment_x, alignment_y = alignment(input_x, input_y)
    end_time = time.time()
    run_time_in_secs = end_time - start_time


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Align two string (Basic Algorithm)')
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
