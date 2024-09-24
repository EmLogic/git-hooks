# git-hooks

A repository providing useful git hooks to be used with [pre-commit](https://pre-commit.com/).
An example on how to execute these hooks in a GitHub Actions workflow is also provided.

pre-commit is a tool for running hooks during certain git actions, such as commit-msg or pre-commit.

- [Hooks in this repo](#hooks-in-this-repo)
  - [apply-commit-message-template](#apply-commit-message-template)
  - [commit-message-checker](#commit-message-checker)
- [Installation](#installation)
  - [1. Install pre-commit](#1-install-pre-commit)
  - [2. Copy hooks config to your repo](#2-copy-hooks-config-to-your-repo)
  - [3. Select hooks](#3-select-hooks)
  - [4. Install hooks](#4-install-hooks)
- [Updating hooks](#updating-hooks)
- [Uninstall hooks](#uninstall-hooks)
- [Commit checker action](#commit-checker-action)

# Hooks in this repo

## apply-commit-message-template

`apply-commit-message-template` ensures every commit has a well-structured commit message by providing a commit message template.
The template is automatically loaded into the commit message editor when the user starts the commit process.

The template commit message is in the `.gitmessage_template` file.

## commit-message-checker

`commit-message-checker` checks whether commit messages adhere to a predefined format. This helps ensure that all commit messages are consistent, readable, and informative.

# Installation

There are four steps in the installation process:

1. Install pre-commit
2. Copy hooks config to your repo
3. Select hooks
4. Install hooks

## 1. Install pre-commit

Hooks in this repo require `pre-commit`.

To install:

```bash
pip install pre-commit
```

## 2. Copy hooks config to your repo

Now you should be ready to install the hooks.

Simply copy `/templates/pre-commit-config.yaml` to the root of your repo:

```bash
cp /templates/pre-commit-config.yaml <path to your repo>/.pre-commit-config.yaml
```

Note the dot in the file name like this `.pre-commit-config.yaml`

## 3. Select hooks

You can use all the hooks listed in `.pre-commit-config.yaml` or only some of them.

Open the file and uncomment those you want to disable with `#`.

```yaml
repos:
  - repo: https://github.com/EmLogic/git-hooks.git
    rev v1.2.3:
    hooks:
      - id: commit-message-checker
      #     - id: apply-commit-message-template     <----- disabled
```

Hooks from other sources can also be added.

## 4. Install hooks

```bash
pre-commit install
```

# Updating hooks

To get the latest hooks version from this repo:

```bash
pre-commit autoupdate
```

It is recommended to run this command after `pre-commit install`

# Uninstall hooks

```bash
pre-commit uninstall
```

# Commit checker action

To check all the commits in a PR, you can include a workflow like the following.
It calls the action in this repo to check the commits messages.

```yaml
name: PR automated checks

on:
  pull_request:
    types: [synchronize, opened]

jobs:
  call-commit-checker:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - uses: EmLogic/git-hooks/actions/check_commit_messages@main
```

It is worth noting that there is a slight difference in the functionality of this action
and the pre-commit hook.

The pre-commit hook allows in addition commits with the "fixup! " prefix. However, this action
does not allow those prefixes, so will fail if a commit has this prefix. The reasoning behind this
is it allows users to create fixup commits with `git commit --fixup <commit SHA>`, but we don't
want these merged to the main branch. To remind users to fixup these commits once a PR is ready for
merging, this action does not allow them.
