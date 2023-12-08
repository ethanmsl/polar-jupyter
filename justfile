# home_dir := env_var('HOME')
local_root := justfile_directory()
invocd_from := invocation_directory()
invoc_is_root := if invocd_from == local_root { "true" } else { "false" }

alias chore := push-chore
alias venv := poet-shell
alias pjf := push-justfile

# Default, lists commands.
_default:
        @just --list --unsorted


# Open Jupyter Lab in a web browser.
open-jupyter: _notify_if_not_root
        @echo "Opening Jupyter Lab in a Web Browser\n"
        poetry run jupyter lab

# Enter Poetry Virtual Environment.
poet-shell: _notify_if_not_root
        @echo "Entering Shell running Poetry Virtual Environment\n"
        poetry shell

# alias ppy='poetry run python3'
# alias ppym='poetry run python3 -m'
# alias ppr='poetry run'


jupy-sync-all: _notify_if_not_root
        #!/bin/bash
        echo "Creating/Syncing Jupytext versions of all '.ipynb' notebooks..."
        for notebook in notebooks/*.ipynb; do
                jupytext --set-formats .ipynb,.ju.py:percent "$notebook"
                jupytext --sync "$notebook"
        done


# TODO: add into poetshell commands
# TODO: join path
# TODO: clean extension
# Sync Jupyter `.ipynb` file with a jupytext file. (For clean diffs and script extensions.)
jupy-sync +NOTEBOOK: _notify_if_not_root
        @echo "Creating/Syncing Jupytext versions of the following '.ipynb' notebooks {{NOTEBOOK}}...\n"
        jupytext --set-formats .ipynb,.ju.py:percent notebooks/{{NOTEBOOK}}.ipynb
        jupytext --sync notebooks/{{NOTEBOOK}}.ipynb

# Runs pre-commit hook. (Linting, testing, doc generation, etc.) Requires poetry shell.
hook: _notify_if_not_root
        @echo "Running git hook from {{local_root}}...\n"
        git hook run pre-commit

# Auto-Gen Files: Add, Commit, and Push all changes.
push-chore: _notify_if_not_root
        @echo "Auto-Gen File Updates: Committing and Pushing all changes to requirments*.txt & dev_docs/*: {{local_root}}...\n"
        git fetch
        git restore --staged .
        git add requirements* dev_docs/*
        git commit --message "chore(auto-gen): requirements files and dev_docs\n\n[note: this is a templated commit]" --no-verify
        git push

# JustFile: Add, Commit, and Push all changes.
push-justfile: _notify_if_not_root
        @echo "JustFile Updates: Committing and Pushing all changes to justfile under root: {{local_root}}...\n"
        git fetch
        git restore --staged .
        git add justfile
        git commit --message "build(auto): updates to justfile (command runner)\n\n[note: this is atemplated commit message]" --no-verify
        git push


notify_text := "\n-----\nNOTE:\n    You are running this command in:\n"+invocd_from+"\n    But it will be run in:\n" +local_root+".\n-----\n"
_notify_if_not_root:
        @echo '{{ if invoc_is_root == 'true' { "" } else { notify_text } }}'


######################### Future Work / Explorations #########################


