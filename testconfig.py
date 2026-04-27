""" This file prints the environment variables associated with each config mode.

Uncomment the setting you want to check, then run:
- python3 testconfig.py

Note: You can only run block one at a time, because os.environ only sets a value once.
Whichever os.environ statement runs first will be the value that's also used in subsequent blocks.
"""

import os
from app.config import get_settings

# # Check "testing" settings
# os.environ["ENVIRONMENT"] = "testing"
# os.environ["DATABASE_URL"] = "sqlite+pysqlite:///:memory:"
# settings = get_settings()
# print('\n', "Printing testing config...")
# for s in settings:
#     print(f'{s[0]}: {s[1]}')

# # Check "development" settings
# os.environ["ENVIRONMENT"] = "development"
# settings = get_settings()
# print('\n', "Printing development config...")
# for s in settings:
#     print(f'{s[0]}: {s[1]}')

# # Check "production" settings
# os.environ["ENVIRONMENT"] = "production"
# settings = get_settings()
# print('\n', "Printing production config...")
# for s in settings:
#     print(f'{s[0]}: {s[1]}')
