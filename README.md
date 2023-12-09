# Polars + Jupyter + lint & type parasable system with JupytText

# QuickStart

- install just & poetry & download this repo
  - if on mac: `brew install just pipx; pipx install poetry`
- open a notebook viewer
  - Web Browser: run `just jupyter`, pick a `.ipynb` file
  - VSCode: open the `notebooks/` directory, pick a `.ipynb` file, click "**Select Kernel**", pick `.venv (Python...)`
- Have fun! -- `shift+enter` runs a cell.

# [Justfile](https://just.systems/)

This project uses a justfile (command runner specification) for convenient CLI operation.
run `just` to see the available commands.

- List of [install options for just](https://github.com/casey/just#packages). (e.g. `brew install just` and `cargo install just`)

# [Poetry](https://python-poetry.org/)

This project uses poetry for virtual environment & dependency management.
The justfile's commands will automatically use the poetry venv when running.

- If working from the CLI: `just venv` or `poetry shell` will enter a venv shell state bringing all dependencies live. (e.g. jupyter, pyright, etc.)
- If working from VSCode: simply selecting the venv associatted kernel will bring the dependencies live.
- install via [pipx](https://pipx.pypa.io/stable/) `pipx install poetry` (pipx is used to install python _applications_. It keeps applications' dependency requirements from shortcircuiting due to one another or other changes to the python global install pool. <-- pipx is to the user what poetry is to the developer)
  - Alternatively you can use a [dedicated poetry installer](https://python-poetry.org/docs/#installing-with-the-official-installer)

# [JupyText](https://jupytext.readthedocs.io/en/latest/)

- Jupyter files (`*.ipynb`) do not offer much visibility with diff and commit tools like git. (Though [custom solutions are being created](https://github.blog/changelog/2023-03-01-feature-preview-rich-jupyter-notebook-diffs/)) Jupytext basically converts the code and cell format to code and markdown. And enables syncing the jupyter `.ipynb` files with jupytext `.ju.py` files.
  - As a plus, jupytext files are also just runnable scripts. So if you want to convert your notebook to a script they're an excellent place to start.
- You can synch via jupyter (with jupytext extensions already added) or you can use the just command runner. `just jsync-all` will synch all the files in the `notebooks/` directory.

# TODO:

- Edit Lint Exceptions to be Notebook friendly
