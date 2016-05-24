#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import unicode_literals
import yaml


print("## Whatis 〜 Questions.")
with open('data/text/WhatIs.yml') as f:
    wis = yaml.load(f.read())
    for word in wis.keys():
        print("  - " + word)

print("")

print("## Can I use 〜 Questions.")
with open('data/text/CanIUse.yml') as f:
    caniuse = yaml.load(f.read())
    for word in caniuse.keys():
        print("  - " + word)
