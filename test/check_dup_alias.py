#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
helpers for amimoto_alexa
"""

from __future__ import print_function
from __future__ import unicode_literals
import yaml
from collections import Counter

flatten=lambda i:[a for b in i for a in(flatten(b)if hasattr(b,'__iter__')else(b,))]

with open('data/aliases.yml') as f:
    aliases = yaml.load(f.read())
    words = filter(None, flatten(aliases.values()))

if len(words) == len(set(words)):
    print("No dup aliases")
else:
    print([words for key,val in Counter(a).items() if val > 2])
    raise StandardError, "found dup aliases!!"
