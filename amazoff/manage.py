#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    if not os.path.isfile(os.path.join("amazoff", "settings", "local.py")):
        print "[Error] No such file : 'amazoff/settings.local.py"
        sys.exit()
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "amazoff.settings.local")
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
