# -*- coding: utf-8 -*-
import os
import time
import sys

def cli_progress_test(end_val, bar_length=20):
    for i in xrange(0, end_val):
        percent = float(i) / end_val
        hashes = '█' * int(round(percent * bar_length))
        spaces = ' ' * (bar_length - len(hashes))
        sys.stdout.write("\rPercent: [{0}] {1}%".format(hashes + spaces, int(round(percent * 100))))
        sys.stdout.flush()


def load(left, right, length, time_space):
    x = 0
    y = ""
    print "\r"
    while x < length:
        space = length - len(y)
        space = " " * space
        z = left + y + space + right
        print "\r", z,
        y += "█"
        time.sleep(time_space)
        x += 1

cli_progress_test(1000)
