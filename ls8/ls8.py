#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

# grab file name to load from sys.argv
file_name = sys.argv[1]

cpu = CPU()

cpu.load(file_name)
cpu.run()