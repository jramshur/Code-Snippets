# CleanNames Power Query Function

## Purpose
The `CleanNames` function standardizes text Names data by:
- Removing **non-alphabetic characters** (except spaces).
- Converting text to **uppercase**.
- Removing specified **abbreviations** (optional, default: `{}` → no abbreviations are removed).
- Removing **single-letter words** (optional, default: `false`).
- Returning a new column with cleaned values.

---

## Function Code
```powerquery
let
    CleanNames = (
        Table as table,
        InputColumn as text,
        OutputColumn as text,
        optional Abbreviations as list,
        optional RemoveSingleLetters as logical
    ) as table =>
    let
        // Set default values if optional parameters are missing
        AbbreviationsList = if Abbreviations = null then {} else Abbreviations,
        RemoveSingleLettersFlag = if RemoveSingleLetters = null then false else RemoveSingleLetters,

        // Apply cleaning transformation in a single step
        ProcessedTable = Table.AddColumn(
            Table,
            OutputColumn,
            each if Record.Field(_, InputColumn) <> null
                then
                    let
                        // Keep only letters and spaces, convert to uppercase
                        CleanedText = Text.Upper(Text.Select(Record.Field(_, InputColumn), {"A".."Z", "a".."z", " "})),
                        
                        // Remove abbreviations and optionally remove single-letter words
                        ProcessedText = Text.Combine(
                            List.Select(
                                Text.Split(CleanedText, " "),
                                each (not List.Contains(AbbreviationsList, _)) and (not RemoveSingleLettersFlag or Text.Length(_) > 1)
                            ),
                            " "
                        )
                    in
                        ProcessedText
                else null,
            type text
        )
    in
        ProcessedTable
in
    CleanNames
```

---

## Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| **Table** | table | ✅ Yes | The input table containing the column to be cleaned. |
| **InputColumn** | text | ✅ Yes | The name of the column to clean. |
| **OutputColumn** | text | ✅ Yes | The name of the new column to store the cleaned values. |
| **Abbreviations** | list | ❌ No | A list of words (e.g., titles) to remove. Default: `{}` (empty list, meaning no words are removed). |
| **RemoveSingleLetters** | logical | ❌ No | If `true`, removes single-letter words. Default: `false`. |

---

## Returns
- A table with all original columns **plus a new column (`OutputColumn`) containing the cleaned text**.

---

## Example Usage

### 1️⃣ Default Behavior (No abbreviations removed, single-letter words kept)
```powerquery
let
    CleanedTable = CleanNames(#"Source Table", "OriginalTextColumn", "CleanedTextColumn")
in
    CleanedTable
```

### 2️⃣ Remove Specific Abbreviations
```powerquery
let
    CustomAbbreviations = {"MD", "DR", "JR"},
    CleanedTable = CleanNames(#"Source Table", "OriginalTextColumn", "CleanedTextColumn", CustomAbbreviations)
in
    CleanedTable
```

### 3️⃣ Remove Single-Letter Words
```powerquery
let
    CleanedTable = CleanNames(#"Source Table", "OriginalTextColumn", "CleanedTextColumn", null, true)
in
    CleanedTable
```

### 4️⃣ Fully Custom Call
```powerquery
let
    CustomAbbreviations = {"MD", "DR", "PHD"},
    CleanedTable = CleanNames(#"Source Table", "OriginalTextColumn", "CleanedTextColumn", CustomAbbreviations, true)
in
    CleanedTable
```

---

## Function Logic
1. **Cleans Text:**  
   - Removes all non-alphabetic characters **except spaces**.  
   - Converts text to **uppercase**.  
2. **Splits Text into Words** (by spaces).  
3. **Removes Abbreviations** (if provided, otherwise none are removed).  
4. **Removes Single-Letter Words** (if enabled).  
5. **Combines Words Back into a Cleaned Text Value**.  

---

## Notes
- null values are ignored and blank/empty values do not get special handling
- This function **preserves null values** (does not convert them to empty strings).
- Words are matched **exactly** (e.g., `"DR"` is removed if specified, but `"DRAKE"` remains).
- Works with **any column name**—simply provide the appropriate names when calling the function.
- Defaults ensure **no abbreviations are removed**, and **single-letter words are kept** unless explicitly removed.


