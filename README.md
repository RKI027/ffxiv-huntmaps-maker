# ffxiv-huntmaps-maker

Library + CLI to annotate FFXIV in-game map assets with Elite Marks spawn positions.

## Installation

- Clone repo
- cd to directory

### Option 1: Using uv (Recommended)

[uv](https://docs.astral.sh/uv/) is a fast Python package installer and project manager.

- Install uv if you haven't already: `curl -LsSf https://astral.sh/uv/install.sh | sh` (or see [uv installation docs](https://docs.astral.sh/uv/getting-started/installation/))
- Run commands directly with `uv run`:
  - `uv run annotate.py` to get a list of commands
  - `uv run annotate.py check_files` to run a specific command

### Option 2: Using pip

- switch to any virtual/conda environment you'd like to use (or not). Package is tested for python >= 3.10
- `pip install -r requirements.txt`
- `python annotate.py` to get a list of commands

## How to use

##### Configuration files

- `config.yaml`: used to set paths, annotation styles, legend configuration and position and some game-related metadata we can't extract from the game (mapping map::expansion and map::landmine)
- `zone_info.yaml`: holds map information extracted from the game. This file is generated once using tools provided by the package then edited manually as needed (rarely).
- `marks.json`: holds the marks information (name, rank, zone and spawn locations). Maintained manually as new marks are released or locations are updated.

##### Workflow

The package expects clean zone map files to be located under the same path that TexTools use by default to extract assets. For maps, it looks like:

`{textools_base_folder}\Saved\UI\Maps\{region}\{zone}\`

TexTools will extract to this path under `{filename}.dds`. The package will expect the clean file to be available at `{filename}_backup.dds` and save the annotated map at `{filename}.dds` so it's ready to import (just a click on `Load` in TexTools since it's the default name).

So the process is:

- extract each map with TexTools
- run the `check_files` and `backup_files` command
- proceed with annotations

**NOTE 1**: once you save annotated maps, you **shouldn't** run again the `backup_files` or you would lose your copy of the original files and need to extract them again

**NOTE 2**: when saving annotated maps, it will save a copy in the original place (for easy import with TexTools) and two copies (format `dds` for the game and format `bnp` for preview) in the companion repo (`project_path` in `config.yaml`) from which we release the mod.

#### As a CLI

The process is the following:

##### Configuration
1. Edit `data/config.yaml` to adjust to your preferences, especially the paths and the marker/legend styles.
2. review `zone_info.yaml` in case the asset path in the game files has changed: occasionally, SE will move a map from zonename to "zonename 00". Remove/Add/Amend a zonename entry for the zones concerned if needed. If the zonename entry doesn't exist, the script will use the true zone name.

##### Assets

As explained above:

3. Using TexTools, export the dds for each map: just `Save As` and accept the default path and file name.
4. Assuming you just exported the original dds map files, run: `uv run annotate.py check_files` and, assuming this came out without any error, run `uv run annotate.py backup_files`. From there, you're ready to work. 
   
##### Execution
5. Run `uv run annotate.py annotate_map zone_name` to annotate that zone. It will open a view of the annotated map without saving. You can check the outcome and adjust.
6. Once ready, run `uv run annotate.py annotate_all`. All maps will be rendered and saved (both in the project path and in original asset path)
7. Optionally, if needed, you can annotate and save a single map with:
   
   `uv run annotate.py annotate_map zone_name --save`.

##### Using the modified maps
8. With TexTools, either (consult textools doc for precise how-to):
    * import the new dds files
    * create a mod pack with the new dds files.

#### As a library

It can also be used as a library. The **configuration**, **assets** and **use** steps are the same as above. For execution, for example:

from a jupyter notebook created in the same directory:

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
```

## Development

If you want to contribute or modify the code:

### Install with dev dependencies

```bash
uv sync --extra dev
# or with `pip`
pip install -r requirements-dev.txt
```

This installs the project along with development tools like `ruff` (linting/formatting) and `pytest` (testing).

### Code quality checks

```bash
# Check code with ruff
uv run ruff check *.py

# Auto-format code with ruff
uv run ruff format *.py

# Check formatting without modifying files
uv run ruff format --check *.py
```

### Running tests

```bash
uv run pytest
# or with pip
python -m pytest tests/ -v
```

See `tests/README.md` for more details.

## To Dos

* **Improve the workflow w.r.t the backup files [#8](https://github.com/RKI027/ffxiv-huntmaps-maker/issues/8)**:
   - changing `backup` to `orig` or `original` to better reflect the purpose
   - better handling in the case of the backup already existing: we want to be able to overwrite a backup in case the actual game map changed but avoid overwriting it if the backup source is an annotated map (since we save the annotated map with the same name). This would be made moot with 3.
   - if no better solution, we should at least have better warnings (as per linked issue)
* **Automate the extraction of assets [#4](https://github.com/RKI027/ffxiv-huntmaps-maker/issues/4)**: if we could use TexTools or a substitute as a CLI (only linux afaik) or as a library, we could avoid the manual use of TexTools for asset extraction and have a better UI to handle map changes.
* **Automate the creation of the modpack [#3](https://github.com/RKI027/ffxiv-huntmaps-maker/issues/3)**: similar to above and would allow automating the release of the modpack from the companion repository.
 
## Disclaimer

Use of the mods created with this tool is at your own risk. Square Enix does not permit the use of any third party tools, even those which do not modify the game. They have stated in interviews that they did not view parsers as a significant problem unless players use them to harass other players.

## Copyright

Copyright @ Arkhelyi, 2020-2025.
