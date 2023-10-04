# Polars + Jupyter + lint & type parasable system with JupytText

dev-notes:
Most of templated systems I have are for running python scripts and terminal apps.
I have a working collection of accessory configs and code for Notebooks, but yet to be formalized.
As such:

- checks may needed to ensure that file-type based lint exceptions in `pyproject.toml` are up to date
- `.ipynb` w/ vscode vs `.ju.py` w/ jupynium or raw nvim is a workflow in progress
  - leaning toward vscode for most work and then manually syncing jupytext files
    - will add a commit hook or linter hook later
    - manual synching (using `percent` format for jupytext):

```zsh
FILEPREFIX=<filename_overlap>
jupytext --set-formats .ipynb,.ju.py:percent $FILEPREFIX.ipynb
jupytext --sync $FILEPREFIX.ipynb
```
