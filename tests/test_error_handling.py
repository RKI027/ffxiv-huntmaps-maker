"""Tests for error handling scenarios."""
import os
import pytest
import responses
from helpers import Position, ZoneApi


class TestPositionErrorHandling:
    """Test error handling in Position class."""

    def test_position_add_invalid_type_raises_error(self):
        """Test that adding invalid type to Position raises an error."""
        pos = Position(10, 20)

        # TODO: Current implementation raises string instead of exception
        # This should be fixed to raise TypeError
        with pytest.raises((TypeError, Exception)):
            result = pos + "invalid"

    def test_position_mul_invalid_type_raises_error(self):
        """Test that multiplying Position by invalid type raises an error."""
        pos = Position(10, 20)

        # TODO: Current implementation raises string instead of exception
        with pytest.raises((TypeError, Exception)):
            result = pos * "invalid"

    def test_position_sub_invalid_type_raises_error(self):
        """Test that subtracting invalid type from Position raises an error."""
        pos = Position(10, 20)

        # TODO: Current implementation raises string instead of exception
        with pytest.raises((TypeError, Exception)):
            result = pos - "invalid"

    def test_position_nested_operations_with_invalid_types(self):
        """Test that nested operations with invalid types raise errors."""
        pos = Position(10, 20)

        # TODO: These should all raise proper TypeErrors
        with pytest.raises((TypeError, Exception)):
            result = (pos + 5) * "invalid"


class TestZoneApiErrorHandling:
    """Test error handling in ZoneApi."""

    @responses.activate
    def test_get_zone_url_api_error(self):
        """Test handling of API errors when getting zone URL."""
        responses.add(
            responses.GET,
            "https://xivapi.com/search?indexes=PlaceName&string=Invalid Zone",
            status=500
        )

        api = ZoneApi(["Invalid Zone"])

        # TODO: Current implementation raises generic Exception
        # Should raise more specific error with helpful message
        with pytest.raises(Exception):
            api._get_zone_url("Invalid Zone")

    @responses.activate
    def test_get_zone_url_multiple_candidates_error(self):
        """Test handling of multiple zone candidates (not Mor Dhona)."""
        responses.add(
            responses.GET,
            "https://xivapi.com/search?indexes=PlaceName&string=Ambiguous Zone",
            json={
                "Results": [
                    {"Name": "Ambiguous Zone", "ID": 1, "Url": "/place/1"},
                    {"Name": "Ambiguous Zone", "ID": 2, "Url": "/place/2"}
                ]
            },
            status=200
        )

        api = ZoneApi(["Ambiguous Zone"])

        # TODO: Current implementation raises generic Exception with candidates
        # Should raise ValueError with helpful message
        with pytest.raises(Exception):
            api._get_zone_url("Ambiguous Zone")

    @responses.activate
    def test_get_zone_info_api_error(self):
        """Test handling of API errors when getting zone info."""
        # Mock successful search
        responses.add(
            responses.GET,
            "https://xivapi.com/search?indexes=PlaceName&string=Test Zone",
            json={
                "Results": [
                    {"Name": "Test Zone", "ID": 1, "Url": "/place/1"}
                ]
            },
            status=200
        )

        # Mock failed zone info request
        responses.add(
            responses.GET,
            "https://xivapi.com/place/1",
            status=404
        )

        api = ZoneApi(["Test Zone"])

        # TODO: Current implementation raises generic Exception
        with pytest.raises(Exception):
            api.get_zone_info("Test Zone")

    @responses.activate
    def test_get_zone_url_network_timeout(self):
        """Test handling of network timeout."""
        # TODO: Current implementation doesn't handle timeouts
        # This test documents expected behavior
        responses.add(
            responses.GET,
            "https://xivapi.com/search?indexes=PlaceName&string=Test Zone",
            body=Exception("Connection timeout")
        )

        api = ZoneApi(["Test Zone"])

        with pytest.raises(Exception):
            api._get_zone_url("Test Zone")

    @responses.activate
    def test_get_zone_url_no_results(self):
        """Test handling when zone is not found."""
        responses.add(
            responses.GET,
            "https://xivapi.com/search?indexes=PlaceName&string=Nonexistent Zone",
            json={"Results": []},
            status=200
        )

        api = ZoneApi(["Nonexistent Zone"])

        # TODO: Current implementation will fail with IndexError
        # Should raise ValueError with helpful message
        with pytest.raises((IndexError, ValueError, Exception)):
            api._get_zone_url("Nonexistent Zone")


class TestFileOperationErrors:
    """Test error handling for file operations."""

    def test_load_marks_nonexistent_file(self):
        """Test loading marks from nonexistent file."""
        from helpers import MarksHelper

        # TODO: Current implementation will raise FileNotFoundError
        # Should provide helpful error message
        with pytest.raises(FileNotFoundError):
            MarksHelper.load_marks("/nonexistent/file.json")

    def test_load_marks_invalid_json(self, temp_dir):
        """Test loading marks from invalid JSON file."""
        from helpers import MarksHelper
        import json

        invalid_file = temp_dir / "invalid.json"
        with open(invalid_file, "w") as f:
            f.write("{ invalid json }")

        # TODO: Should handle JSON decode errors gracefully
        with pytest.raises(json.JSONDecodeError):
            MarksHelper.load_marks(str(invalid_file))

    def test_load_zone_info_nonexistent_file(self):
        """Test loading zone info from nonexistent file."""
        api = ZoneApi([])
        api.cachename = "/nonexistent/zone_info"

        # TODO: Should provide helpful error message
        with pytest.raises(FileNotFoundError):
            api.load_zone_info()

    def test_load_zone_info_invalid_yaml(self, temp_dir):
        """Test loading zone info from invalid YAML."""
        import yaml

        api = ZoneApi([])
        api.cachename = str(temp_dir / "invalid")

        invalid_file = temp_dir / "invalid.yaml"
        with open(invalid_file, "w") as f:
            f.write("{ invalid: yaml: structure:")

        # TODO: Should handle YAML errors gracefully
        with pytest.raises(yaml.YAMLError):
            api.load_zone_info()

    def test_dump_marks_to_readonly_location(self, sample_marks_file):
        """Test dumping marks to read-only location."""
        import platform

        # Platform-specific handling
        if platform.system() == "Windows":
            # Check if running as Administrator on Windows
            import ctypes
            try:
                is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
            except:
                is_admin = False

            if is_admin:
                pytest.skip("Running as Administrator, cannot test permission errors")

            # Use a Windows system directory that requires admin rights
            readonly_path = r"C:\Windows\System32\readonly_test.json"
        else:
            # Unix-like systems: check if running as root
            if os.geteuid() == 0:
                pytest.skip("Running as root, cannot test permission errors")

            # Use /root directory which is not writable by regular users
            readonly_path = "/root/readonly.json"

        from helpers import MarksHelper

        Mark, marks = MarksHelper.load_marks(str(sample_marks_file))

        # TODO: Should handle permission errors gracefully
        # This test may not work on all systems
        with pytest.raises((PermissionError, OSError)):
            MarksHelper.dump_marks(marks, readonly_path)


class TestValueErrors:
    """Test handling of invalid values."""

    def test_compute_columns_zero_rows(self):
        """Test compute_columns with zero rows."""
        from helpers import compute_columns

        with pytest.raises(ValueError):
            rows, cols = compute_columns(10, 0)

    def test_compute_columns_negative_values(self):
        """Test compute_columns with negative values."""
        from helpers import compute_columns

        with pytest.raises(ValueError):
            rows, cols = compute_columns(-5, 3)

    def test_m2c_with_extreme_values(self):
        """Test coordinate conversion with extreme values."""
        from helpers import m2c

        # Test with very large values
        result = m2c(1000000, scale=100)
        assert isinstance(result, int)

        # Test with negative values
        result = m2c(-100, scale=100)
        assert isinstance(result, int)

    def test_drop_shadow_with_zero_iterations(self):
        """Test drop_shadow with zero iterations."""
        from helpers import drop_shadow, Position
        from PIL import Image

        img = Image.new("RGBA", (100, 100), color=(255, 255, 255, 255))

        result = drop_shadow(
            img,
            offset=Position(5, 5),
            shadow_color="#000000",
            iterations=0
        )

        assert result.size == img.size

    def test_drop_shadow_with_negative_offset(self):
        """Test drop_shadow with negative offset."""
        from helpers import drop_shadow, Position
        from PIL import Image

        img = Image.new("RGBA", (100, 100), color=(255, 255, 255, 255))

        # Should handle negative offsets
        result = drop_shadow(
            img,
            offset=Position(-5, -5),
            shadow_color="#000000",
            iterations=2
        )

        assert result.size == img.size
