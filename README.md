# ffxiv-huntmaps-maker

Library + CLI to annotate FFXIV in-game map assets with Elite Marks spawn positions.

## Installation

You need python >= 3.7
Clone repo
switch to any virtual/conda environment you'd like to use (or not)
cd to directory
pip install -r requirements.txt
python annotate.py to get a list of commands

## How to use

The process is the following:

1. Using TexTools, export the dds for each map somewhere (default TexTools path is a good choice)
2. Edit `data/config.yaml` to adjust to your preferences, especially the paths
3. Assuming you just exported the original dds map files, run: `python annotate.py check_files` and, assuming this came out without any error, run `python annotate.py backup_files`. From there, you're ready to work.
4. Edit the marker/legend styles in `data/config.yaml` as desired
5. Run `python annotate.py annotate_map zone_name` to annotate that zone. It will open a view of the annotated map
6. Once ready, run `python annotate.py annotate_all`. All maps will be rendered and saved (both in the project path and in original asset path)
7. With TexTools:

    * import one by one the new dds files
    * (optionally, for distribution), create a mod pack with these assets.

It can also be used as a library, from a jupyter notebook (for exampe) created in the same directory:

```python
from annotate import MapAnnotator

annotator = MapAnnotator()
```

From there, you can call the same methods. `MapAnnotator.annotate_map` will instead preview the output directly in the notebook rather than opening `Paint`.

## Reference

Information on commands, their function and use is available through the tool.

```cmd
python annotate.py [command] --help
```

## To Dos

* [ ] configure linter+black, remote
* [ ] docstrings for helpers.py
* [ ] handle errors
* [ ] write tests
* [ ] write interface to update zone_info
* [ ] method/macro to export all map files. This doesn't seem possible with TexTools. Another [tool](https://github.com/fosspill/FFXIV_Modding_Tool) is in beta and may have that capacity but not yet
* [ ] method/macro to create modpack. Same as above

## Disclaimer

Use of the mods created with this tool is at your own risk. Square Enix does not permit the use of any third party tools, even those which do not modify the game. They have stated in interviews that they did not view parsers as a significant problem unless players use them to harass other players.

## Copyright

Copyright @ Arkhelyi, 2019.
