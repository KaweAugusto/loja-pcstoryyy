#!/usr/bin/env python
import os
import sys

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_ecommerce.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError('Django is required to run this project. Activate your virtualenv and install requirements.') from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
