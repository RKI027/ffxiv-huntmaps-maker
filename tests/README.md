# Test README

## Test Coverage

#### ✅ Working Tests

**Position Class (31 tests)**
- Basic creation and operations
- Addition, subtraction, multiplication (with Position, tuple, scalar)
- Reverse operations (radd, rsub, rmul)
- Negation
- Indexing and iteration
- String representation
- Error handling for addition and subtraction with invalid types ✅

**MarksHelper (4 tests)**
- Loading marks from JSON with UTF-8 encoding ✅
- Loading marks with Unicode characters (Zanig'oh, The Rak'tika Greatwood, etc.) ✅
- Dumping marks to JSON and string ✅
- Preserving Unicode during dump ✅

**ZoneApi (8 tests)**
- Initialization
- Getting zone URLs from API (with mocking)
- Special handling for Mor Dhona
- Getting zone info from API
- Building zone data structure
- Saving/loading zone info as YAML and JSON ✅
- Updating zones dictionary
- Preserving Unicode in zone names ✅

**Coordinate Conversion (4 tests)**
- Map to screen coordinate conversion (m2c)
- Screen to map coordinate conversion (c2m)
- Different scale factors
- Roundtrip conversion

**Helper Functions (7 tests)**
- compute_columns with various inputs
- drop_shadow with basic and radial modes
- drop_shadow with different colors

**Legend Class (2 tests)**
- Basic creation
- Drawing (FAILS - see below)

**Encoding Tests (10 tests)**
- Loading/dumping marks with Unicode characters ✅
- Preserving special characters (apostrophes, etc.) ✅
- Cross-platform encoding consistency ✅
- Parametrized tests for various Unicode zone names ✅

**Error Handling Tests**
- API error scenarios with mocked responses
- File operation errors
- Network timeout handling
- Missing/invalid files

---

#### ⏭️ Skipped Tests

Most MapAnnotator tests are skipped due to complexity requiring:
- Full directory structure setup
- ImageMagick installation
- Complex mocking of file system
- Image file fixtures

These tests document expected behavior but are not currently executable without extensive setup.

---

## Notes

- Tests are written to be independent and can run in any order
- Tests use temporary directories and don't modify existing files
- Mock network requests with `responses` library to avoid external dependencies
- Unicode test data includes real zone/mark names from the game:
  - Zanig'oh
  - The Rak'tika Greatwood
  - Kozama'uka
  - Yak T'el
  - Go'ozoabek'be
  - Xty'iinbek
  - Li'l Murderer
  - Dalvag's Final Flame
  - Emperor's Rose

These tests capture the **current state** of the codebase and will ensure that fixes preserve existing working functionality.
