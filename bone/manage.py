#!/usr/bin/env python
import os
import sys
import signal

# Docker sends SIGTERM instead of SIGINT, this captures both and exits quickly
# http://blog.lotech.org/fix-djangos-runserver-when-run-under-docker-or-pycharm.html

def exit_handler(signum, frame):
    sys.exit(1)

if __name__ == "__main__":
    signal.signal(signal.SIGTERM, exit_handler)
    signal.signal(signal.SIGINT, exit_handler)

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bone.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
