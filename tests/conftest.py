"""Pytest configuration and fixtures for testing."""

import json
import tempfile
from pathlib import Path
import pytest
from PIL import Image
import yaml


@pytest.fixture
def temp_dir(tmp_path):
    """Create a temporary directory for test files."""
    return tmp_path


@pytest.fixture
def sample_marks_data():
    """Sample marks data for testing."""
    return [
        {
            "name": "Test Mark A",
            "rank": "A",
            "zone": "Test Zone",
            "spawns": [[10.0, 20.0], [15.0, 25.0]],
        },
        {
            "name": "Test Mark B",
            "rank": "B",
            "zone": "Test Zone",
            "spawns": [[30.0, 40.0]],
        },
        {
            "name": "Test Mark S",
            "rank": "S",
            "zone": "Test Zone",
            "spawns": [[50.0, 60.0]],
        },
    ]


@pytest.fixture
def sample_marks_file(temp_dir, sample_marks_data):
    """Create a temporary marks.json file."""
    marks_file = temp_dir / "marks.json"
    with open(marks_file, "w", encoding="utf-8") as f:
        json.dump(sample_marks_data, f)
    return marks_file


@pytest.fixture
def sample_marks_data_with_unicode():
    """Sample marks data with Unicode characters."""
    return [
        {
            "name": "Zanig'oh",
            "rank": "A",
            "zone": "The Rak'tika Greatwood",
            "spawns": [[10.0, 20.0]],
        },
        {
            "name": "Go'ozoabek'be",
            "rank": "B",
            "zone": "Kozama'uka",
            "spawns": [[30.0, 40.0]],
        },
        {
            "name": "Xty'iinbek",
            "rank": "S",
            "zone": "Yak T'el",
            "spawns": [[50.0, 60.0]],
        },
    ]


@pytest.fixture
def sample_marks_file_with_unicode(temp_dir, sample_marks_data_with_unicode):
    """Create a temporary marks.json file with Unicode characters."""
    marks_file = temp_dir / "marks_unicode.json"
    with open(marks_file, "w", encoding="utf-8") as f:
        json.dump(sample_marks_data_with_unicode, f)
    return marks_file


@pytest.fixture
def sample_zone_info():
    """Sample zone info data for testing."""
    return {
        "Test Zone": {
            "region": "Test Region",
            "scale": 100,
            "filename": "testzone",
            "expansion": "ARR",
            "legend": {"rows": 4, "position": [100, 100]},
        }
    }


@pytest.fixture
def sample_zone_info_file(temp_dir, sample_zone_info):
    """Create a temporary zone_info.yaml file."""
    zone_file = temp_dir / "zone_info.yaml"
    with open(zone_file, "w", encoding="utf-8") as f:
        yaml.safe_dump(sample_zone_info, f)
    return zone_file


@pytest.fixture
def sample_config():
    """Sample config data for testing."""
    import platform

    # Choose font based on platform
    if platform.system() == "Windows":
        font_path = r"C:\Windows\Fonts\arial.ttf"
    else:
        font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

    # Skip if font doesn't exist
    if not Path(font_path).exists():
        pytest.skip(f"Font file not found: {font_path}")

    return {
        "tool": {
            "textools_path": "~/Documents/TexTools",
            "project_path": "~/Documents/Projects/ffxiv-huntmaps",
            "imagemagick_path": None,
            "preview_url_template": "https://example.com/{region}/{zone}/{file}_m.png",
        },
        "marker": {
            "size": 40,
            "inner_size_scale": 0.4,
            "shadow_offset": [3, 3],
            "shadow_scale": 1.0,
            "shadow_color": "#737373",
            "shadow_iterations": 7,
            "shadow_direction": "radial",
        },
        "legend": {
            "inner_offset": [15, 15],
            "shadow_offset": [1, 1],
            "column_spacing": 30,
            "line_spacing": 7,
            "mark_scale": 0.95,
            "font_stroke": 1,
            "border_space": [5, 5],
            "font_size": 30,
            "font": font_path,
            "shadow_color": "#444444",
            "shadow_iterations": 7,
        },
        "colors": {
            "B1": "lightblue",
            "B2": "royalblue",
            "A1": "orange",
            "A2": "yellow",
            "S": "red",
            "SS": "#ff0099",
            "SSs": "#ff99ff",
        },
        "expansions": {"ARR": "A Realm Reborn", "HW": "Heavensward"},
        "zones": {
            "Test Zone": {
                "expansion": "ARR",
                "landmine": False,
                "legend": {"rows": 4, "position": [100, 100]},
            }
        },
    }


@pytest.fixture
def sample_config_file(temp_dir, sample_config):
    """Create a temporary config.yaml file."""
    config_file = temp_dir / "config.yaml"
    with open(config_file, "w", encoding="utf-8") as f:
        yaml.safe_dump(sample_config, f)
    return config_file


@pytest.fixture
def sample_image():
    """Create a sample RGBA image for testing."""
    img = Image.new("RGBA", (2048, 2048), color=(255, 255, 255, 255))
    return img


@pytest.fixture
def sample_image_file(temp_dir, sample_image):
    """Create a temporary image file."""
    img_file = temp_dir / "test_map.png"
    sample_image.save(img_file)
    return img_file
