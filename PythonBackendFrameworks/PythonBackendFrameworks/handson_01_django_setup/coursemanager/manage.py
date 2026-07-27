#!/usr/bin/env python
"""manage.py — role: CLI entry point for Django admin commands (runserver, migrate, ...)."""
import os
import sys


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "coursemanager.settings")
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
