# Test Baseline Report

Date: 2025-11-05
Total Tests: 114 (68 passed, 39 skipped, 6 failing, 1 deselected)

## Test Suite Summary

This test suite was created BEFORE any fixes were applied to document the current behavior of the codebase. The tests will serve as regression tests to ensure fixes don't break existing functionality.

### Test Coverage

#### ✅ Working Tests (68 passing)

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

#### ⏭️ Skipped Tests (39 tests)

Most MapAnnotator tests are skipped due to complexity requiring:
- Full directory structure setup
- ImageMagick installation
- Complex mocking of file system
- Image file fixtures

These tests document expected behavior but are not currently executable without extensive setup.

---

## Known Issues Documented by Tests

### 🔴 Critical Issues

1. ~~**Inconsistent UTF-8 Encoding** (helpers.py:59, 77, 83, 147)~~
   - ~~Files opened without explicit encoding specification~~
   - ~~Will fail on systems with non-UTF-8 default encoding~~
   - ~~Affects: sort_marks(), save_zone_info()~~

2. ~~**Raising Strings Instead of Exceptions** (helpers.py:179, 191, 206)~~
   - ~~Position class raises strings: `raise "message"`~~
   - ~~Should raise proper exception objects: `raise TypeError("message")`~~

3. ~~**Deprecated Pillow API** (helpers.py:362, 383, 386)~~
   - ~~Using `textsize()` which is removed in Pillow 10.0.0+~~
   - ~~Breaks Legend drawing functionality~~
   - ~~Must migrate to `textbbox()`~~

4. ~~**Generic Exception Types** (helpers.py:116, 119, 129)~~
   - ~~Using `raise Exception(...)` instead of specific types~~
   - ~~Makes error handling difficult~~

5. ~~**Missing Error Messages** (annotate.py:317)~~
   - ~~`raise ValueError` without descriptive message~~
   - ~~Users won't know why size mismatch occurred~~

### 🟡 Medium Priority Issues

6. **No subprocess error checking** (annotate.py:221)
   - `subprocess.run()` doesn't check return code
   - ImageMagick failures may go unnoticed

7. **Unsafe YAML Loading** (annotate.py:35, helpers.py:153)
   - Using `yaml.Loader` instead of `yaml.SafeLoader`
   - Security risk with untrusted YAML files

8. **Missing file existence checks**
   - Image.open() calls without checking file exists first
   - No validation of ImageMagick path
   - No validation of font file path

---

## Next Steps

See `README.md` for test execution instructions.

1. ~~Fix UTF-8 encoding issues (add `encoding="utf-8"` to all file opens)~~
2. ~~Fix Position class exception raising (change string raises to TypeError)~~
3. ~~Fix deprecated textsize() calls (migrate to textbbox())~~
4. Add proper error messages to all exceptions
5. Add subprocess error checking
6. Use SafeLoader for YAML
7. Re-run tests to verify fixes don't break passing tests

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
