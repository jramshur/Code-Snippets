# Replace column values based on mapping table

This document explains how to use the `ReplaceValuesInColumn` function in Power Query to replace values in a specific column based on a mapping table. The function takes a source table, the name of the column to process, and a replacement table with `OldValue` and `NewValue` columns as inputs.

---

## Function Overview

### Inputs
- **SourceTable**: The table containing the data to modify.
- **ColumnName**: The name of the column in the `SourceTable` where replacements will occur.
- **ReplacementsTable**: A table containing two columns:
  - `OldValue`: The values to be replaced.
  - `NewValue`: The new values to replace the old ones.

### Output
- A modified table where the specified column has values replaced based on the mapping provided in `ReplacementsTable`.

---

## Function Definition

```m
let
    ReplaceValuesInColumn = (SourceTable as table, ColumnName as text, ReplacementsTable as table) =>
    let
        // Ensure ColumnName exists in SourceTable
        ValidateColumn = Table.SelectColumns(SourceTable, {ColumnName}),
        
        // Apply replacements
        ReplacedTable = List.Accumulate(
            Table.ToRows(ReplacementsTable),
            SourceTable,
            (currentTable, replacementRow) =>
                Table.ReplaceValue(
                    currentTable,
                    replacementRow{0},  // OldValue
                    replacementRow{1},  // NewValue
                    Replacer.ReplaceText,
                    {ColumnName}
                )
        )
    in
        ReplacedTable
in
    ReplaceValuesInColumn
```
### Potential improvements to function
Consider adding option to replace entire cell value or replace subtext. The current implementation will only replace subtext within the cell value. This is due to using Replacer.ReplaceValue() function. To replace entire cell value instead use Replacer.ReplaceValue().

```m
Table.ReplaceValue(
    currentTable,
    replacementRow{0},  // OldValue
    replacementRow{1},  // NewValue
    Replacer.Value,
    {ColumnName}
)
```

## Example Usage

### Sample Tables

#### 1. Source Table (`DataTable`)


| ID   | ColumnToReplace | OtherColumn |
|------|-----------------|-------------|
| 1    | A               | 123         |
| 2    | B               | 456         |
| 3    | C               | 789         |


#### 2. Replacement/Mapping Table


| OldValue | NewValue |
|----------|----------|
| A        | Alpha    |
| B        | Beta     |
| C        | Gamma    |



### Using the function

To use the function, invoke it as follows:

``` powerquery
let
    ReplacedTable = ReplaceValuesInColumn(DataTable, "ColumnToReplace", Replacements)
in
    ReplacedTable
 ```


### Resulting Table


| ID   | ColumnToReplace | OtherColumn |
|------|-----------------|-------------|
| 1    | Alpha           | 123         |
| 2    | Beta            | 456         |
| 3    | Gamma           | 789         |


----------

## How It Works

1.  **Input Validation**:
    -   Ensures the column specified in `ColumnName` exists in `SourceTable`.
2.  **Replacement Logic**:
    -   Uses `List.Accumulate` to iterate through each row of `ReplacementsTable`.
    -   For each `OldValue`, replaces occurrences in the specified column with the corresponding `NewValue`.
3.  **Output**:
    -   Returns the modified table with the replacements applied.


## Notes

-   **Case Sensitivity**: Replacements are case-sensitive. Ensure consistency in `OldValue` and the column values.
-   **Dynamic Replacements**: The function dynamically handles multiple replacement pairs from the `ReplacementsTable`.


## Limitations

-   The function assumes the column in `ColumnName` exists in `SourceTable`. If the column does not exist, an error will occur.
-   The `ReplacementsTable` must contain exactly two columns: `OldValue` and `NewValue`.


## Use Cases

-   **Data Cleaning**: Replace inconsistent or incorrect values in a dataset.
-   **Mapping Transformations**: Standardize values based on predefined mappings.
-   **Dynamic Updates**: Automate value replacement in large datasets.

