#! /usr/bin/env python

"""
This script validates Git commit messages based on a specific format as part of a pre-commit hook.
The expected format is <type>(<scope>): <subject>, where 'type' is one of the predefined categories (feat, fix, docs, etc.).
This helps ensure that all commit messages adhere to a standard that supports automatic changelog generation and more readable history.
The script reads the commit message from a file, validates it against the expected format, and exits with status 1 if the message does not comply, providing a prompt for correction.
"""

import re
import sys
import argparse
from pathlib import Path


def commit_msg_is_valid(input_file, allow_prefix: bool) -> bool:

    with open(input_file) as file:
        commit_message = file.read().strip()

    # Regex to match <type>(<scope>): <subject>
    # Explanation:
    # ^ - Start of the line
    # (feat|fix|docs|style|refactor|test|chore|build) - Matches allowed types
    # \([^)]+\) - Matches '(', followed by any characters except ')', and then a ')'.
    # : - Matches the colon following the scope
    # \s - Matches any whitespace character (like space)
    # .+ - Matches one or more of any character (the subject)
    if not re.match(r"^(feat|fix|docs|style|refactor|test|chore|build)\([^)]+\): \S.*", commit_message):

        if re.match(r"^(Revert )", commit_message):
            return True

        if allow_prefix:
            if not re.match(r"^fixup! ", commit_message):
                return False
        else:
            return False

    return True


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    # Add a required positional argument
    parser.add_argument('input_file', help='Commit message file')

    # Make this disallow so the default without this flag to have fixup! commits allowed
    # This simplifies the pre-commit interface for general use
    parser.add_argument(
        "--disallow_fixup",
        action="store_true",
        help="Flag for specifying if fixup! commits are allowed or not"
    )
    args = parser.parse_args()

    if not commit_msg_is_valid(input_file=args.input_file, allow_prefix=(not args.disallow_fixup)):
        with open(args.input_file) as file:
            commit_message = file.read().strip()
            print(f'\033[31mCommit message is invalid:\n\n"{commit_message}"\033[0m', end="")
        sys.exit(1)
