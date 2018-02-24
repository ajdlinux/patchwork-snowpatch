#!/usr/bin/python3
# Patchwork - automated patch tracking system
# Copyright (C) 2018 Daniel Axtens <dja@axtens.net>
#
# This file is part of the Patchwork package.
#
# Patchwork is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Patchwork is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

import sys
import os
import mailbox

usage = """Split a maildir or mbox into N mboxes
in an alternating pattern

Usage: ./split_mail.py <input> <mbox prefix> <N>

 <input>: input mbox file or Maildir
 <mbox prefix>: output mbox
    <mbox-prefix>-1... must not exist
 <N> N-way split"""


if len(sys.argv) != 4:
    print(usage)
    exit(1)

in_name = sys.argv[1]
out_name = sys.argv[2]

try:
    n = int(sys.argv[3])
except ValueError:
    print("N must be an integer.")
    print(" ")
    print(usage)
    exit(1)

if n < 2:
    print("N must be be at least 2")
    print(" ")
    print(usage)
    exit(1)

if not os.path.exists(in_name):
    print("No input at ", in_name)
    print(" ")
    print(usage)
    exit(1)

print("Opening", in_name)
if os.path.isdir(in_name):
    inmail = mailbox.Maildir(in_name)
else:
    inmail = mailbox.mbox(in_name)

out = []
for i in range(n):
    if os.path.exists(out_name + "-" + str(i + 1)):
        print("mbox already exists at ", out_name + "-" + str(i + 1))
        print(" ")
        print(usage)
        exit(1)

    out += [mailbox.mbox(out_name + '-' + str(i + 1))]

print("Copying messages")

for (i, msg) in enumerate(inmail):
    out[i % n].add(msg)

print("Done")
