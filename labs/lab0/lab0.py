# This is the file you'll use to submit most of Lab 0.

# Certain problems may ask you to modify other files to accomplish a certain
# task. There are also various other files that make the problem set work, and
# generally you will _not_ be expected to modify or even understand this code.
# Don't get bogged down with unnecessary work.


# Section 1: Problem set logistics ___________________________________________

# This is a multiple choice question. You answer by replacing
# the symbol 'fill-me-in' with a number, corresponding to your answer.

# You get to check multiple choice answers using the tester before you
# submit them! So there's no reason to worry about getting them wrong.
# Often, multiple-choice questions will be intended to make sure you have the
# right ideas going into the problem set. Run the tester right after you
# answer them, so that you can make sure you have the right answers.

# What version of Python do we *recommend* (not "require") for this course?
#   1. Python v2.3
#   2. Python v2.5 or Python v2.6
#   3. Python v3.0
# Fill in your answer in the next line of code ("1", "2", or "3"):

ANSWER_1 = "2"


# Section 2: Programming warmup _____________________________________________

# Problem 2.1: Warm-Up Stretch
import math


def cube(x):
    return x ** 3


# Cheat way
def factorial_import(x):
    return math.factorial(x)


# Probably a more intended way
def factorial(x):
    if x < 0:
        raise ValueError("x must be non-negative")

    out = 1
    for i in range(1, x + 1):
        out *= i

    return out


def count_pattern(pattern, lst):
    n_matches = 0
    for i in range(len(lst)):
        check_lst = lst[i : i + len(pattern)]
        if len(pattern) != len(check_lst):
            break

        match = True
        for p, l in zip(pattern, check_lst):
            if p != l:
                match = False
                break

        if match:
            n_matches += 1

    return n_matches


# Problem 2.2: Expression depth


def depth(expr, cur_depth=0):
    if isinstance(expr, (list, tuple)):
        cur_depth += 1
        return max(depth(e, cur_depth) for e in expr)
    else:
        return cur_depth


# Problem 2.3: Tree indexing


def tree_ref(tree, index):
    tree_subset = tree.copy()
    for i in index:
        tree_subset = tree_subset[i]

    return tree_subset


# Section 3: Symbolic algebra

# Your solution to this problem doesn't go in this file.
# Instead, you need to modify 'algebra.py' to complete the distributor.

from algebra import Sum, Product, simplify_if_possible
from algebra_utils import distribution, encode_sumprod, decode_sumprod
