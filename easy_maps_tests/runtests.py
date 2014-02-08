#!/usr/bin/env python
import sys
from django.core.management import execute_manager
import settings

sys.argv.insert(1, 'test')

if len(sys.argv) == 2:
    sys.argv.append('easy_maps')
    sys.argv.append('test_app')

if __name__ == "__main__":
    execute_manager(settings)

