# ffxiv-huntmaps-maker

Library + CLI to annotate FFXIV in-game map assets with Elite Marks spawn positions.

## Installation

### Option 1: Using uv (Recommended)

[uv](https://docs.astral.sh/uv/) is a fast Python package installer and project manager.

- You need python >= 3.10
- Clone repo
- cd to directory
- Install uv if you haven't already: `curl -LsSf https://astral.sh/uv/install.sh | sh` (or see [uv installation docs](https://docs.astral.sh/uv/getting-started/installation/))
- Run commands directly with `uv run`:
  - `uv run annotate.py` to get a list of commands
  - `uv run annotate.py check_files` to run a specific command
- Or install as a CLI tool:
  - `uv tool install .` (from the project directory)
  - `ffxiv-huntmaps` to get a list of commands

### Option 2: Using pip

- You need python >= 3.10
- Clone repo
- switch to any virtual/conda environment you'd like to use (or not)
- cd to directory
- `pip install -r requirements.txt`
- `python annotate.py` to get a list of commands

## How to use

The process is the following:

1. Using TexTools, export the dds for each map somewhere (default TexTools path is a good choice)
2. Edit `data/config.yaml` to adjust to your preferences, especially the paths
3. Assuming you just exported the original dds map files, run: `uv run annotate.py check_files` (or `python annotate.py check_files` if using pip) and, assuming this came out without any error, run `uv run annotate.py backup_files`. From there, you're ready to work.
4. review `zone_info.yaml` in case the asset path in the game files has changed (occasionally, SE will move a map from zonename to "zonename 00"). Remove/Add/Amend a zonename entry for the zones concerned if needed. If the zonename entry doesn't exist, the script will use the true zone name.
5. Edit the marker/legend styles in `data/config.yaml` as desired
6. Run `uv run annotate.py annotate_map zone_name` to annotate that zone. It will open a view of the annotated map
7. Once ready, run `uv run annotate.py annotate_all`. All maps will be rendered and saved (both in the project path and in original asset path)
8. With TexTools:

    * import one by one the new dds files
    * (optionally, for distribution), create a mod pack with these assets.

It can also be used as a library, from a jupyter notebook (for exampe) created in the same directory:

```python
from annotate import MapAnnotator

annotator = MapAnnotator()
```

From there, you can call the same methods. `MapAnnotator.annotate_map` will instead preview the output directly in the notebook rather than opening `Paint`.

## Blending

See [this](https://github.com/RKI027/ffxiv-huntmaps/blob/master/Blended/README.md) for information about preparation for blending.

## Reference

Information on commands, their function and use is available through the tool.

```cmd
uv run annotate.py [command] --help
# or with pip:
python annotate.py [command] --help
# or if installed with uv tool:
ffxiv-huntmaps [command] --help
```

## To Dos

* [ ] handle errors
* [ ] write tests

## Disclaimer

Use of the mods created with this tool is at your own risk. Square Enix does not permit the use of any third party tools, even those which do not modify the game. They have stated in interviews that they did not view parsers as a significant problem unless players use them to harass other players.

## Copyright

Copyright @ Arkhelyi, 2020.
