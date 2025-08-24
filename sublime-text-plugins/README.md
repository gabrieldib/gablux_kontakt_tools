# Sublime Text Plugin: Add Hashed Function IDs

This Sublime Text plugin scans your currently active file for `function` declarations, automatically prepends each function name with a unique hash-based ID, and stores metadata about each transformation in a persistent database.

### ✨ Features

* Automatically renames function declarations to include a hashed prefix:

  ```
  function my_func
  ↓
  function fn_a1b2c3_my_func
  ```
* Ensures each function name is uniquely tagged.
* Skips functions that have already been processed.
* Saves a persistent database of all hashed functions to `User/hashed_functions_dB.json`.
* Provides a summary report via dialog or output panel after each run.

---

### Example DB Structure (`hashed_functions_dB.json`)

```json
{
  "fn_a1b2c3_my_func": {
    "original_name": "my_func",
    "creation_timestamp": "1724613204.534",
    "function_original_file": "my_script.ksp"
  }
}
```

---

### How to Use

1. Save this file in your Sublime Text `Packages/User` directory as `add_function_id.py`.
2. Open the command palette (`Ctrl+Shift+P` or `Cmd+Shift+P` on macOS).
3. Run: **`Add Function Id`**
4. The plugin will:

   * Modify function names to include a unique hash
   * Update the backing database
   * Save the file
   * Show a report of changes

---

### Collision Handling

The plugin uses a SHA-256 hash based on the function name and current timestamp to generate a 6-character prefix. If a collision ever occurs, it retries until uniqueness is guaranteed.

---

### Skipping Logic

The plugin will **not reprocess** functions that:

* Already follow the pattern `fn_XXXXXX_...`
* Exist in the JSON database
* Match the current file name

---

### Notes

* You can reset the plugin by deleting `Packages/User/hashed_functions_dB.json`.
* Supports `.ksp` and any other script-based formats with `function` declarations.

---

### License

MIT License — free to use, modify, and distribute.
