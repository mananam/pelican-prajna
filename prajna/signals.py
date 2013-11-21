# -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function
from blinker import signal

# Generator-level signals
sloka_generator_init = signal('sloka_generator_init')
sloka_generator_finalized = signal('sloka_generator_finalized')

# Page-level signals
sloka_generator_preread = signal('sloka_generator_preread')
sloka_generator_context = signal('sloka_generator_context')
