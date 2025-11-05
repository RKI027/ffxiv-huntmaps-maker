"""Tests for helpers module."""
import pytest
import json
import yaml
from pathlib import Path
from PIL import Image
import responses

from helpers import (
    Position, MarksHelper, ZoneApi,
    m2c, c2m, compute_columns, drop_shadow, Legend
)


class TestPosition:
    """Tests for Position class."""

    def test_position_creation(self):
        """Test Position object creation."""
        pos = Position(10, 20)
        assert pos.x == 10
        assert pos.y == 20

    def test_position_add_position(self):
        """Test adding two Position objects."""
        pos1 = Position(10, 20)
        pos2 = Position(5, 15)
        result = pos1 + pos2
        assert result.x == 15
        assert result.y == 35

    def test_position_add_tuple(self):
        """Test adding Position with tuple."""
        pos = Position(10, 20)
        result = pos + (5, 15)
        assert result.x == 15
        assert result.y == 35

    def test_position_add_scalar(self):
        """Test adding Position with scalar."""
        pos = Position(10, 20)
        result = pos + 5
        assert result.x == 15
        assert result.y == 25

    def test_position_radd(self):
        """Test reverse addition."""
        pos = Position(10, 20)
        result = (5, 15) + pos
        assert result.x == 15
        assert result.y == 35

    def test_position_mul_position(self):
        """Test multiplying two Position objects."""
        pos1 = Position(10, 20)
        pos2 = Position(2, 3)
        result = pos1 * pos2
        assert result.x == 20
        assert result.y == 60

    def test_position_mul_tuple(self):
        """Test multiplying Position with tuple."""
        pos = Position(10, 20)
        result = pos * (2, 3)
        assert result.x == 20
        assert result.y == 60

    def test_position_mul_scalar(self):
        """Test multiplying Position with scalar."""
        pos = Position(10, 20)
        result = pos * 2
        assert result.x == 20
        assert result.y == 40

    def test_position_rmul(self):
        """Test reverse multiplication."""
        pos = Position(10, 20)
        result = 2 * pos
        assert result.x == 20
        assert result.y == 40

    def test_position_sub_position(self):
        """Test subtracting Position objects."""
        pos1 = Position(10, 20)
        pos2 = Position(3, 5)
        result = pos1 - pos2
        assert result.x == 7
        assert result.y == 15

    def test_position_sub_tuple(self):
        """Test subtracting tuple from Position."""
        pos = Position(10, 20)
        result = pos - (3, 5)
        assert result.x == 7
        assert result.y == 15

    def test_position_sub_scalar(self):
        """Test subtracting scalar from Position."""
        pos = Position(10, 20)
        result = pos - 5
        assert result.x == 5
        assert result.y == 15

    def test_position_rsub(self):
        """Test reverse subtraction."""
        pos = Position(10, 20)
        result = (15, 30) - pos
        assert result.x == 5
        assert result.y == 10

    def test_position_neg(self):
        """Test negation of Position."""
        pos = Position(10, 20)
        result = -pos
        assert result.x == -10
        assert result.y == -20

    def test_position_getitem(self):
        """Test indexing Position."""
        pos = Position(10, 20)
        assert pos[0] == 10
        assert pos[1] == 20

    def test_position_setitem(self):
        """Test setting Position values by index."""
        pos = Position(10, 20)
        pos[0] = 30
        pos[1] = 40
        assert pos.x == 30
        assert pos.y == 40

    def test_position_iter(self):
        """Test iterating over Position."""
        pos = Position(10, 20)
        values = list(pos)
        assert values == [10, 20]

    def test_position_repr(self):
        """Test Position string representation."""
        pos = Position(10, 20)
        assert repr(pos) == "Position(10,20)"

    def test_position_add_invalid_type(self):
        """Test adding Position with invalid type raises error."""
        pos = Position(10, 20)
        # TODO: Current implementation raises a string instead of an exception
        # This test documents the current behavior
        with pytest.raises(TypeError):
            result = pos + "invalid"

    def test_position_mul_invalid_type(self):
        """Test multiplying Position with invalid type raises error."""
        pos = Position(10, 20)
        # TODO: Current implementation raises a string instead of an exception
        with pytest.raises(TypeError):
            result = pos * "invalid"

    def test_position_sub_invalid_type(self):
        """Test subtracting invalid type from Position raises error."""
        pos = Position(10, 20)
        # TODO: Current implementation raises a string instead of an exception
        with pytest.raises(TypeError):
            result = pos - "invalid"


class TestMarksHelper:
    """Tests for MarksHelper class."""

    def test_load_marks_basic(self, sample_marks_file):
        """Test loading marks from JSON file."""
        Mark, marks = MarksHelper.load_marks(str(sample_marks_file))

        assert len(marks) == 3
        assert marks[0].name == "Test Mark A"
        assert marks[0].rank == "A"
        assert marks[0].zone == "Test Zone"
        assert marks[0].spawns == [[10.0, 20.0], [15.0, 25.0]]

    def test_load_marks_with_unicode(self, sample_marks_file_with_unicode):
        """Test loading marks with Unicode characters."""
        Mark, marks = MarksHelper.load_marks(str(sample_marks_file_with_unicode))

        assert len(marks) == 3
        assert marks[0].name == "Zanig'oh"
        assert marks[0].zone == "The Rak'tika Greatwood"
        assert marks[1].name == "Go'ozoabek'be"
        assert marks[1].zone == "Kozama'uka"

    def test_dump_marks(self, temp_dir, sample_marks_data):
        """Test dumping marks to JSON file."""
        # First load to create namedtuples
        marks_file = temp_dir / "input.json"
        with open(marks_file, "w", encoding="utf-8") as f:
            json.dump(sample_marks_data, f)

        Mark, marks = MarksHelper.load_marks(str(marks_file))

        # Dump to new file
        output_file = temp_dir / "output.json"
        MarksHelper.dump_marks(marks, str(output_file))

        # Verify output
        with open(output_file, "r", encoding="utf-8") as f:
            result = json.load(f)

        assert len(result) == 3
        assert result[0]["name"] == "Test Mark A"

    def test_dump_marks_to_string(self, sample_marks_file):
        """Test dumping marks to string."""
        Mark, marks = MarksHelper.load_marks(str(sample_marks_file))
        result = MarksHelper.dump_marks(marks, "str")

        assert isinstance(result, str)
        data = json.loads(result)
        assert len(data) == 3


class TestZoneApi:
    """Tests for ZoneApi class."""

    def test_zone_api_init(self):
        """Test ZoneApi initialization."""
        zones = ["Test Zone 1", "Test Zone 2"]
        api = ZoneApi(zones)

        assert api.zones == zones
        assert api.base_url == "https://xivapi.com"
        assert api.cachename == "data/zone_info"

    @responses.activate
    def test_get_zone_url_success(self):
        """Test getting zone URL from API."""
        # Mock the API response
        responses.add(
            responses.GET,
            "https://xivapi.com/search?indexes=PlaceName&string=Test Zone",
            json={
                "Results": [
                    {"Name": "Test Zone", "ID": 1, "Url": "/placename/1"}
                ]
            },
            status=200
        )

        api = ZoneApi(["Test Zone"])
        url = api._get_zone_url("Test Zone")

        assert url == "/placename/1"

    @responses.activate
    def test_get_zone_url_mor_dhona(self):
        """Test getting zone URL for Mor Dhona (special case)."""
        # Mock the API response with multiple results
        responses.add(
            responses.GET,
            "https://xivapi.com/search?indexes=PlaceName&string=Mor Dhona",
            json={
                "Results": [
                    {"Name": "Mor Dhona", "ID": 25, "Url": "/placename/25"},
                    {"Name": "Mor Dhona", "ID": 26, "Url": "/placename/26"}
                ]
            },
            status=200
        )

        api = ZoneApi(["Mor Dhona"])
        url = api._get_zone_url("Mor Dhona")

        assert url == "/placename/26"

    @responses.activate
    def test_get_zone_info_success(self):
        """Test getting zone info from API."""
        # Mock search response
        responses.add(
            responses.GET,
            "https://xivapi.com/search?indexes=PlaceName&string=Test Zone",
            json={
                "Results": [
                    {"Name": "Test Zone", "ID": 1, "Url": "/placename/1"}
                ]
            },
            status=200
        )

        # Mock zone info response
        responses.add(
            responses.GET,
            "https://xivapi.com/placename/1",
            json={
                "Maps": [
                    {
                        "PlaceNameRegion": {"Name": "Test Region"},
                        "SizeFactor": 100,
                        "MapFilenameId": "test/zone"
                    }
                ]
            },
            status=200
        )

        api = ZoneApi(["Test Zone"])
        info = api.get_zone_info("Test Zone")

        assert info["PlaceNameRegion"]["Name"] == "Test Region"
        assert info["SizeFactor"] == 100

    def test_get_zone_data(self):
        """Test building zone data structure."""
        api = ZoneApi([])
        info = {
            "PlaceNameRegion": {"Name": "Test Region"},
            "SizeFactor": 100,
            "MapFilenameId": "test/zone"
        }

        result = api.get_zone_data(info)

        assert result["region"] == "Test Region"
        assert result["scale"] == 100
        assert result["filename"] == "testzone"

    def test_save_and_load_zone_info_yaml(self, temp_dir, sample_zone_info):
        """Test saving and loading zone info as YAML."""
        api = ZoneApi(["Test Zone"])
        api.cachename = str(temp_dir / "zone_info")

        # Save
        api.save_zone_info(sample_zone_info, as_json=False)

        # Load
        result = api.load_zone_info()

        assert result["Test Zone"]["region"] == "Test Region"
        assert result["Test Zone"]["scale"] == 100

    def test_save_and_load_zone_info_json(self, temp_dir, sample_zone_info):
        """Test saving zone info as JSON."""
        api = ZoneApi(["Test Zone"])
        api.cachename = str(temp_dir / "zone_info")

        # Save
        api.save_zone_info(sample_zone_info, as_json=True)

        # Verify file exists
        json_file = temp_dir / "zone_info.json"
        assert json_file.exists()

        # Verify content
        with open(json_file, "r", encoding="utf-8") as f:
            result = json.load(f)

        assert result["Test Zone"]["region"] == "Test Region"

    def test_load_zone_info_updates_zones(self, temp_dir, sample_zone_info):
        """Test load_zone_info updates zones dict."""
        api = ZoneApi(["Test Zone"])
        api.cachename = str(temp_dir / "zone_info")

        # Save first
        api.save_zone_info(sample_zone_info, as_json=False)

        # Load with zones dict
        zones = {"Test Zone": {"extra_key": "value"}}
        api.load_zone_info(zones)

        assert zones["Test Zone"]["region"] == "Test Region"
        assert zones["Test Zone"]["extra_key"] == "value"


class TestCoordinateConversion:
    """Tests for coordinate conversion functions."""

    def test_m2c_basic(self):
        """Test map to screen coordinate conversion."""
        # At position 1, should be 0
        result = m2c(1, scale=100)
        assert result == 0

        # Test other values
        result = m2c(21, scale=100)
        assert isinstance(result, int)
        assert result > 0

    def test_m2c_different_scales(self):
        """Test m2c with different scale factors."""
        result_100 = m2c(10, scale=100)
        result_200 = m2c(10, scale=200)

        # Different scales should give different results
        assert result_100 != result_200

    def test_c2m_basic(self):
        """Test screen to map coordinate conversion."""
        # At position 0, should be 1
        result = c2m(0, scale=100)
        assert result == 1

        # Test other values
        result = c2m(1000, scale=100)
        assert result > 1

    def test_m2c_c2m_roundtrip(self):
        """Test that m2c and c2m are inverse operations."""
        original = 15.5
        screen = m2c(original, scale=100)
        back = c2m(screen, scale=100)

        # Should be approximately equal (rounding may cause small difference)
        assert abs(back - original) < 0.1


class TestComputeColumns:
    """Tests for compute_columns function."""

    def test_compute_columns_basic(self):
        """Test basic column computation."""
        rows, cols = compute_columns(12, 3)
        assert rows == 3
        assert cols == 4

    def test_compute_columns_with_remainder(self):
        """Test column computation with remainder."""
        rows, cols = compute_columns(10, 3)
        assert rows == 3
        assert cols == 4  # Need 4 columns for 10 items in 3 rows

    def test_compute_columns_more_rows_than_items(self):
        """Test when requested rows exceed items."""
        rows, cols = compute_columns(5, 10)
        assert rows == 5
        assert cols == 1

    def test_compute_columns_exact_fit(self):
        """Test when items fit exactly."""
        rows, cols = compute_columns(9, 3)
        assert rows == 3
        assert cols == 3


class TestDropShadow:
    """Tests for drop_shadow function."""

    def test_drop_shadow_basic(self, sample_image):
        """Test basic drop shadow creation."""
        result = drop_shadow(
            sample_image,
            offset=Position(5, 5),
            shadow_color="#000000",
            iterations=3,
            scale=1,
            direction=None
        )

        assert result.size == sample_image.size
        assert result.mode == "RGBA"

    def test_drop_shadow_radial(self, sample_image):
        """Test radial drop shadow."""
        result = drop_shadow(
            sample_image,
            offset=Position(5, 5),
            shadow_color="#000000",
            iterations=3,
            scale=1,
            direction="radial"
        )

        assert result.size == sample_image.size
        assert result.mode == "RGBA"

    def test_drop_shadow_different_colors(self, sample_image):
        """Test drop shadow with different colors."""
        # Create image with some content
        img = Image.new("RGBA", (100, 100), color=(0, 0, 0, 0))
        from PIL import ImageDraw
        draw = ImageDraw.Draw(img)
        draw.ellipse([25, 25, 75, 75], fill=(255, 0, 0, 255))

        result = drop_shadow(
            img,
            offset=Position(3, 3),
            shadow_color="#FF0000",
            iterations=2,
            scale=1,
            direction=None
        )

        assert result.size == img.size


class TestLegend:
    """Tests for Legend class."""

    def test_legend_creation(self, sample_config):
        """Test Legend object creation."""
        legend = Legend(sample_config)

        assert legend.inner_offset.x == 15
        assert legend.inner_offset.y == 15
        assert legend.column_space == 30
        assert legend.line_space == 7

    def test_legend_draw(self, sample_config):
        """Test drawing a legend."""
        legend = Legend(sample_config)
        marks = {
            "Test Mark A": "A1",
            "Test Mark B": "B1",
            "Test Mark S": "S"
        }

        result = legend.draw(
            img_size=(2048, 2048),
            position=Position(100, 100),
            marks=marks,
            rows=3
        )

        assert result.size == (2048, 2048)
        assert result.mode == "RGBA"
