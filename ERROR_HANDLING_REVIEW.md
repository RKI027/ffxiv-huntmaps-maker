# Error Handling Review and Improvement Tracking

**Goal**: Make error messages helpful for debugging when things fail, especially with external tools and file operations.

**Not aiming for perfection** - just clear error messages that point users in the right direction.

---

## Priority Areas

### 1. Configuration File Issues

**Current State**: Limited error handling when config files are missing or malformed

#### ~~1.1 Missing config.yaml~~ ✅ FIXED
- **Location**: `annotate.py:34`
- **Issue**: FileNotFoundError with no context
- **Impact**: User doesn't know what file is missing or where it should be
- **Fix Applied**: Added try-except block with clear error message

#### 1.2 Invalid YAML syntax
- **Location**: `annotate.py:34-36`
- **Issue**: yaml.YAMLError with cryptic message
- **Impact**: User doesn't understand what's wrong with their config
- **Suggested Fix**: Catch yaml.YAMLError and provide guidance:
  ```
  "Invalid YAML syntax in 'data/config.yaml' at line X: {error}
   Check for proper indentation and syntax."
  ```

#### 1.3 Missing required config keys
- **Location**: `annotate.py:38-46`
- **Issue**: KeyError with no context about missing keys
- **Impact**: User doesn't know which config value is missing
- **Suggested Fix**: Catch KeyError and indicate required fields:
  ```
  "Missing required configuration key: '{key}' in data/config.yaml.
   Please check your configuration file."
  ```

#### 1.4 Invalid color names
- **Location**: Used throughout marker/legend drawing
- **Issue**: Pillow raises ValueError for invalid colors
- **Impact**: Unclear which color specification is wrong
- **Suggested Fix**: Validate colors at startup or catch ValueError during drawing:
  ```
  "Invalid color value '{color}' for rank '{rank}' in config.yaml.
   Use named colors (e.g., 'red') or hex codes (e.g., '#FF0000')."
  ```

#### 1.5 Font file not found
- **Location**: `helpers.py:331-336` (already has good error handling!)
- **Status**: ✅ GOOD - Already has clear error message
- **Example**: This is what we want elsewhere!

#### 1.6 ImageMagick path validation
- **Location**: `annotate.py:48-56` (already has good error handling!)
- **Status**: ✅ GOOD - Already validates path and provides clear message

---

### 2. Data File Issues

#### 2.1 Missing marks.json
- **Location**: `helpers.py:66`, `annotate.py:61`
- **Issue**: FileNotFoundError with no context
- **Impact**: User doesn't know where marks file should be
- **Suggested Fix**: Catch FileNotFoundError:
  ```
  "Marks data file not found: {filename}.
   Please ensure data/marks.json exists."
  ```

#### 2.2 Invalid JSON in marks.json
- **Location**: `helpers.py:66-67`
- **Issue**: json.JSONDecodeError with limited context
- **Impact**: User doesn't know how to fix the JSON
- **Suggested Fix**: Catch json.JSONDecodeError:
  ```
  "Invalid JSON in marks file '{filename}' at line {lineno}: {msg}.
   Please check the file format."
  ```
- **Test Coverage**: Already tested in `tests/test_error_handling.py:160-171`

#### 2.3 Empty marks.json
- **Location**: `helpers.py:69-70`
- **Issue**: IndexError when accessing marks[0]
- **Impact**: Unclear error about empty file
- **Suggested Fix**: Check if marks list is empty:
  ```
  "Marks file '{filename}' is empty or has no valid mark entries.
   Please ensure the file contains valid mark data."
  ```

#### 2.4 Missing zone_info.yaml
- **Location**: `helpers.py:163`, `annotate.py:59`
- **Issue**: FileNotFoundError with no context
- **Impact**: User doesn't know this file needs to exist
- **Suggested Fix**: Catch FileNotFoundError:
  ```
  "Zone information file not found: {cachename}.yaml.
   Please ensure data/zone_info.yaml exists."
  ```
- **Test Coverage**: Already tested in `tests/test_error_handling.py:173-180`

#### 2.5 Invalid YAML in zone_info.yaml
- **Location**: `helpers.py:163-164`
- **Issue**: yaml.YAMLError with cryptic message
- **Suggested Fix**: Catch yaml.YAMLError:
  ```
  "Invalid YAML in zone info file at line {line}: {error}.
   Please check the file format."
  ```
- **Test Coverage**: Already tested in `tests/test_error_handling.py:182-195`

---

### 3. Map File Operations

#### 3.1 Missing backup files
- **Location**: `annotate.py:158-163` (already has good error handling!)
- **Status**: ✅ GOOD - Clear message telling user to run backup_files() first
- **Example**: This is good error handling!

#### 3.2 Missing source files for backup
- **Location**: `annotate.py:148-150`
- **Issue**: FileNotFoundError during shutil.copy with no context
- **Impact**: User doesn't know which zone's source file is missing
- **Suggested Fix**: Wrap in try-except per zone:
  ```
  "Source map file not found for zone '{name}': {path}.
   Please ensure you've exported the map from TexTools."
  ```

#### 3.3 Permission errors during backup
- **Location**: `annotate.py:150`
- **Issue**: PermissionError with no guidance
- **Impact**: User doesn't know they need write permissions
- **Suggested Fix**: Catch PermissionError:
  ```
  "Permission denied when creating backup for '{name}': {path}.
   Please check file and directory permissions."
  ```

#### 3.4 Disk space issues during save
- **Location**: `annotate.py:235`, `annotate.py:248-249`, `annotate.py:252`
- **Issue**: OSError with unclear message
- **Impact**: User doesn't know disk is full
- **Suggested Fix**: Catch OSError during save operations:
  ```
  "Failed to save map '{name}': {error}.
   Check available disk space and permissions."
  ```

#### 3.5 Missing directories for project saves
- **Location**: `annotate.py:248` (already handles with exist_ok=True!)
- **Status**: ✅ GOOD - Creates directories automatically

---

### 4. ImageMagick Integration

#### 4.1 ImageMagick conversion failure
- **Location**: `annotate.py:238-245` (already has excellent error handling!)
- **Status**: ✅ EXCELLENT - Provides command, return code, and stderr
- **Example**: This is exactly what we want! Shows the command that failed and the error output

#### 4.2 ImageMagick not in PATH
- **Location**: `annotate.py:44-46`, validated at `annotate.py:48-56`
- **Status**: ✅ GOOD - Already handled with clear message

---

### 5. Network/API Errors (ZoneApi)

**Note**: These operations interact with external API (xivapi.com) which is inherently unreliable

#### 5.1 Network timeout
- **Location**: `helpers.py:104`, `helpers.py:128`
- **Issue**: requests may hang or raise Timeout with unclear context
- **Impact**: User doesn't know if it's their network or the API
- **Suggested Fix**: Add timeout parameter and catch exceptions:
  ```
  resp = requests.get(url, timeout=30)

  except requests.Timeout:
    raise RuntimeError(
      "Request to xivapi.com timed out for zone '{name}'.
       Check your internet connection or try again later."
    )
  except requests.ConnectionError:
    raise RuntimeError(
      "Failed to connect to xivapi.com for zone '{name}'.
       Check your internet connection."
    )
  ```
- **Test Coverage**: Already documented in `tests/test_error_handling.py:115-128`

#### 5.2 API HTTP errors
- **Location**: `helpers.py:120-123`, `helpers.py:132-135` (already has error handling!)
- **Status**: ✅ GOOD - Provides HTTP status code
- **Possible Enhancement**: Could include response body for more context
- **Test Coverage**: Already tested in `tests/test_error_handling.py:48-112`

#### 5.3 No results from zone search
- **Location**: `helpers.py:119`
- **Issue**: IndexError when candidates[0] accessed on empty list
- **Impact**: Unclear why zone wasn't found
- **Suggested Fix**: Check if candidates is empty:
  ```
  if not candidates:
    raise ValueError(
      "Zone '{name}' not found on xivapi.com.
       Check the zone name spelling."
    )
  ```
- **Test Coverage**: Already documented in `tests/test_error_handling.py:131-145`

#### 5.4 Multiple zone candidates (ambiguous)
- **Location**: `helpers.py:116-118` (already has error handling!)
- **Status**: ✅ GOOD - Raises ValueError with candidates shown
- **Test Coverage**: Already tested in `tests/test_error_handling.py:65-84`

#### 5.5 Unexpected API response format
- **Location**: `helpers.py:106`, `helpers.py:130`
- **Issue**: KeyError if API changes response structure
- **Impact**: Cryptic error about missing key
- **Suggested Fix**: Catch KeyError during response parsing:
  ```
  try:
    results = resp.json()["Results"]
  except KeyError:
    raise RuntimeError(
      "Unexpected response format from xivapi.com for zone '{name}'.
       The API may have changed."
    )
  ```

---

### 6. Image Operations

#### 6.1 Invalid image format
- **Location**: `annotate.py:164`, `annotate.py:349`
- **Issue**: PIL.UnidentifiedImageError with unclear context
- **Impact**: User doesn't know which file is corrupted
- **Suggested Fix**: Catch PIL exceptions:
  ```
  try:
    map_layer = Image.open(map_path)
  except PIL.UnidentifiedImageError:
    raise ValueError(
      "Cannot open map file for '{name}': {map_path}.
       File may be corrupted or in an unsupported format."
    )
  ```

#### 6.2 Image size mismatch (blend operation)
- **Location**: `helpers.py:352-355` (already has good error handling!)
- **Status**: ✅ GOOD - Clear message about size mismatch

#### 6.3 Missing blend mask files
- **Location**: `annotate.py:343-347` (already has good error handling!)
- **Status**: ✅ GOOD - Clear message about missing mask and expected expansion

---

### 7. Type Validation Issues

#### 7.1 Position class type errors
- **Location**: `helpers.py:183-231`
- **Issue**: Operations raise TypeError but current implementation works
- **Status**: ⚠️ REVIEW - Test file notes "raises string instead of exception"
- **Test Coverage**: Tests in `tests/test_error_handling.py:8-43` document current behavior
- **Note**: Tests indicate "TODO: Current implementation raises string instead of exception"
- **Investigation Needed**: Check if Position actually raises proper TypeErrors

#### 7.2 Invalid values in compute_columns
- **Location**: `helpers.py:255-262`
- **Issue**: No validation of inputs; may cause ZeroDivisionError or invalid results
- **Impact**: Negative or zero values could break legend layout
- **Suggested Fix**: Add input validation:
  ```
  if n_rows <= 0 or n_items < 0:
    raise ValueError(
      f"Invalid grid parameters: n_items={n_items}, n_rows={n_rows}.
       Both must be positive."
    )
  ```
- **Test Coverage**: Already documented in `tests/test_error_handling.py:236-259`

---

### 8. Invalid Zone/Mark References

#### 8.1 Invalid zone name in commands
- **Location**: `annotate.py:153` (annotate_map), `annotate.py:320` (blend_map)
- **Issue**: KeyError when zone not in self._zones
- **Impact**: Unclear if zone name is misspelled or not configured
- **Suggested Fix**: Catch KeyError and provide guidance:
  ```
  try:
    scale = self._zones[name]["scale"]
  except KeyError:
    available = ", ".join(sorted(self._zones.keys()))
    raise ValueError(
      f"Unknown zone '{name}'. Available zones: {available}"
    )
  ```

#### 8.2 Zone with no marks
- **Location**: `annotate.py:169-176`
- **Issue**: Silent - creates empty annotation
- **Impact**: User might not realize something is wrong
- **Suggested Fix**: Log warning or check:
  ```
  zone_marks = self._get_zone_marks(name, True)
  if not zone_marks:
    import warnings
    warnings.warn(f"No marks found for zone '{name}'")
  ```

---

## Summary Statistics

- ✅ **Already Good**: 7 areas have good error handling
- ⚠️ **Needs Improvement**: 15+ areas could benefit from better messages
- 🔴 **High Priority**: Configuration files, missing data files, network errors
- 🟡 **Medium Priority**: File operations, invalid inputs
- 🟢 **Low Priority**: Edge cases, validation improvements

---

## Implementation Strategy

1. **Phase 1 - Quick Wins** (High ROI):
   - Add try-except blocks around config file loading with clear messages
   - Validate zone names with helpful error listing available zones
   - Add timeout to API requests and handle common network errors

2. **Phase 2 - File Operations**:
   - Improve error messages for missing/invalid data files
   - Better handling of permission errors during backup/save
   - Validate file format when opening images

3. **Phase 3 - Polish**:
   - Input validation for edge cases
   - Warnings for suspicious situations (empty marks, etc.)
   - API response format validation

---

## Testing

Existing test coverage in `tests/test_error_handling.py` already documents many issues:
- Position type errors (lines 8-43)
- ZoneApi network/API errors (lines 45-146)
- File operation errors (lines 148-231)
- Value validation errors (lines 233-305)

These tests serve as excellent documentation of current behavior and can be updated as improvements are made.

---

## Notes

- The code already has several examples of good error handling (ImageMagick validation, font file checks, blend mask validation)
- Focus should be on making errors actionable - tell the user what to check or fix
- Don't need to handle every edge case - just the common failure modes
- External tools (ImageMagick, xivapi.com, TexTools) are the main sources of failures
