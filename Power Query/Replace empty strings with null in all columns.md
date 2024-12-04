
# ReplaceEmptyStringsWithNull Function Documentation

## Overview
The `ReplaceEmptyStringsWithNull` function processes a table in Power Query, replacing all occurrences of empty strings (`""`) with `null` in columns of type `nullable text`. The use of `nullable text` is critical due to the behavior of the `Table.ColumnsOfType` function, which requires an exact match of both data type and nullability to identify columns.

For a detailed discussion on this topic, see [Pitfalls with Table.ColumnsOfType](https://ssbi-blog.de/blog/technical-topics-english/pitfalls-with-table-columnsoftype/).

---

## Why Use `nullable text`?
When using the Power Query function `Table.ColumnsOfType`, nullability plays a crucial role. This function requires an **exact match** for both the type (e.g., `text`) and the nullability (`nullable`). Here are key points that explain this behavior:

1. **Nullability Matters:** If a column is of type `text` but nullable (`nullable text`), the `Table.ColumnsOfType` function will not recognize it unless the nullability is specified explicitly.
2. **UI Behavior:** Power Query's UI frequently assigns `nullable` types to columns (e.g., via `Table.TransformColumnTypes`) even if the M code does not explicitly indicate nullability. For example, a column defined as `text` in the UI will internally be treated as `nullable text`.
3. **Precision Required:** If `Table.ColumnsOfType` is used without accounting for nullability, the function may fail to identify the intended columns. For instance, specifying `{type text}` instead of `{type nullable text}` will result in no matches for columns processed through the UI.

### Example Problem
In a scenario where a column is marked as `text` in the UI but internally treated as `nullable text`, using:

```m
Table.ColumnsOfType(table, {type text})
```

... will fail to detect such columns.

### Solution
To ensure the desired columns are correctly identified, use:

```m
Table.ColumnsOfType(table, {type nullable text})
```

By explicitly specifying nullability, the function behaves as expected, and all relevant columns are processed correctly.

---

## Function Definition
```m
let
    ReplaceEmptyStringsWithNull = (inputTable as table) as table =>
    let
        // Get the names of nullable text columns directly
        textColumnNames = Table.ColumnsOfType(inputTable, {type nullable text}),

        // Replace empty strings with null in text columns
        replacedTable = List.Accumulate(
            textColumnNames,
            inputTable,
            (currentTable, columnName) => 
                Table.ReplaceValue(
                    currentTable, 
                    "", 
                    null, 
                    Replacer.ReplaceValue, 
                    {columnName}
                )
        )
    in
        replacedTable
in
    ReplaceEmptyStringsWithNull
```

---

## Example Usage
```m
let
    // Input Table
    InputTable = Table.FromRecords({
        [Column1 = "", Column2 = 123, Column3 = "Text"],
        [Column1 = "Data", Column2 = 456, Column3 = ""]
    }),

    // Applying the Function
    ResultTable = ReplaceEmptyStringsWithNull(InputTable)
in
    ResultTable
```

---

## Input Example
| Column1 | Column2 | Column3 |
|---------|---------|---------|
| ""      | 123     | Text    |
| Data    | 456     | ""      |

---

## Output Example
| Column1 | Column2 | Column3 |
|---------|---------|---------|
| null    | 123     | Text    |
| Data    | 456     | null    |

---

## Key Takeaways
1. **Importance of Nullability:** The behavior of `Table.ColumnsOfType` makes it essential to specify `nullable text` instead of just `text` when dealing with columns processed through Power Query's UI or `Table.TransformColumnTypes`.
2. **Debugging Tip:** Use `Table.Schema` to inspect column types and nullability when issues arise with `Table.ColumnsOfType`.
3. **Best Practices:** Always consider nullability when working with Power Query's type-sensitive functions to ensure consistent results.

## Reference
For more details on the importance of nullability and pitfalls with `Table.ColumnsOfType`, see [Pitfalls with Table.ColumnsOfType](https://ssbi-blog.de/blog/technical-topics-english/pitfalls-with-table-columnsoftype/).

This awareness ensures the function behaves reliably across varied scenarios.
