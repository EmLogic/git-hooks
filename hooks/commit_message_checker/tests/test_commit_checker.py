#! /usr/bin/env python

"""
This script is used for testing the commit checker
It takes a list of commit messages to check from the test_commits.yml file,
so if you want to add more checks you can add them there.
"""

from pathlib import Path
import yaml
from enum import Enum

import sys
import os

# Since we are in a subdirectory need to add the parent folder to the path
# to access the commit_msg_checker script
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
import commit_msg_checker

class TestStatus(Enum):
    PASS = "pass"
    FAIL = "fail"

TEST_COMMIT_FILE_NAME = "test_commit_message"
THIS_DIRECTORY = Path(__file__).parent
COMMIT_MESSAGE_FILE = THIS_DIRECTORY.joinpath(TEST_COMMIT_FILE_NAME)

def run_test(commit_msg: str, should_pass: bool, allow_fixup: bool) -> TestStatus:

    COMMIT_MESSAGE_FILE.write_text(commit_msg)

    commit_msg_is_valid = commit_msg_checker.commit_msg_is_valid(input_file=COMMIT_MESSAGE_FILE,
                                                                 allow_prefix=allow_fixup)

    status = TestStatus.PASS

    if should_pass and (not commit_msg_is_valid):
        print(f"'{commit_msg}' should pass")
        status = TestStatus.FAIL

    if (not should_pass) and commit_msg_is_valid:
        print(f"'{commit_msg}' should fail")
        status = TestStatus.FAIL

    return status

def run_test_list(allowed_types: list[str], test_list: list[str], should_pass: bool, allow_fixup: bool) -> TestStatus:

    test_status = TestStatus.PASS

    for test in test_list:

        if "<type>" in test:

            for type in allowed_types:

                test_with_type = test.replace("<type>", type)

                result = run_test(commit_msg=test_with_type, should_pass=should_pass, allow_fixup=allow_fixup)
                if result == TestStatus.FAIL:
                    test_status = TestStatus.FAIL

        else:
            result = run_test(commit_msg=test, should_pass=should_pass, allow_fixup=allow_fixup)
            if result == TestStatus.FAIL:
                test_status = TestStatus.FAIL

    return test_status


def test_commit_checker(allow_fixup: bool) -> TestStatus:

    test_commits_file = THIS_DIRECTORY.joinpath("test_commits.yml")

    with open(test_commits_file, 'r') as file:
        test_commits: dict = yaml.safe_load(file)

    allowed_types = test_commits.get('allowed_types')
    should_pass_list: list[str] = test_commits.get('should_pass')
    should_fail_list: list[str] = test_commits.get('should_fail')

    should_pass_with_fixup_allowed_list: list[str] = test_commits.get('should_pass_with_fixup_allowed')
    if allow_fixup:
        should_pass_list.extend(should_pass_with_fixup_allowed_list)
    else:
        should_fail_list.extend(should_pass_with_fixup_allowed_list)

    overall_status = TestStatus.PASS

    if run_test_list(
        allowed_types=allowed_types, test_list=should_pass_list,
        should_pass=True, allow_fixup=allow_fixup
    ) == TestStatus.FAIL:
        overall_status = TestStatus.FAIL

    if run_test_list(
        allowed_types=allowed_types, test_list=should_fail_list,
        should_pass=False, allow_fixup=allow_fixup
    ) == TestStatus.FAIL:
        overall_status = TestStatus.FAIL

    COMMIT_MESSAGE_FILE.unlink()

    print(f"Test Script Result: {overall_status}")

    return overall_status


if __name__ == "__main__":

    print("Running checker with fixup allowed:")
    status_with_fixup_allowed = test_commit_checker(allow_fixup=True)

    print("Running checker with fixup disallowed:")
    status_with_fixup_disallowed = test_commit_checker(allow_fixup=False)

    if (status_with_fixup_allowed == TestStatus.FAIL or
        status_with_fixup_disallowed == TestStatus.FAIL
    ):
        exit(1)
