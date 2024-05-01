
# Power Query M Code for Duplicating Rows Based on value in another column

## Overview

This documentation outlines the process of duplicating rows in a Power Query table based on the value specified in the "Frequency" column. This technique is useful for data preparation tasks where entries need to be repeated a certain number of times for further analysis or processing.

## Example Source Table

The initial data table includes the following columns:
- `CustomerID`: Unique identifier for the customer.
- `Product`: Name of the product purchased.
- `Frequency`: Number of times the row should be duplicated.

| CustomerID | Product | Frequency |
|:----------:|---------|:---------:|
| 1          | Widget  | 3         |
| 2          | Gadget  | 2         |
| 3          | Gizmo   | 4         |

## Power Query M Code

```
let
    // Sample source data
    Source = Table.FromRecords([
        [CustomerID = 1, Product = "Widget", Frequency = 3],
        [CustomerID = 2, Product = "Gadget", Frequency = 2],
        [CustomerID = 3, Product = "Gizmo", Frequency = 4]
    ]),
    
    // Add an empty list as a helper column, where each list's length is based on Frequency
    AddEmptyList = Table.AddColumn(Source, "Custom", each List.Repeat({""}, [Frequency])),

    // Expand the newly added list column to duplicate rows
    ExpandEmptyList = Table.ExpandListColumn(AddEmptyList, "Custom"),

    // Remove the now unnecessary columns after expansion
    RemovedColumns = Table.RemoveColumns(ExpandEmptyList, {"Frequency", "Custom"})
in
    RemovedColumns
```
## Output Table

After applying the Power Query M code, the output table will show each row duplicated according to the "Frequency" column from the original source data. Below is the expected output:

| CustomerID | Product |
|:----------:|---------|
| 1 | Widget |
| 1 | Widget |
| 1 | Widget |
| 2 | Gadget |
| 2 | Gadget |
| 3 | Gizmo |
| 3 | Gizmo |
| 3 | Gizmo |
| 3 | Gizmo |


## Explanation

1.  **Source**: Defines the initial dataset.
2.  **AddEmptyList**: Adds a column named "Custom" where each entry is a list of empty strings. The length of each list corresponds to the value in the "Frequency" column.
3.  **ExpandEmptyList**: Expands the "Custom" column, duplicating each row according to its respective frequency.
4.  **RemovedColumns**: Cleans up by removing the "Custom" and "Frequency" columns, leaving only the duplicated rows based on the original frequency.
