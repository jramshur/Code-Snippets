# GetRowErrors Function Documentation
*A reusable Power Query (M) function for flattening row‑level errors into an audit log*

---

## Purpose
When Power Query encounters a value that cannot be converted to the expected data type it stores an **Error** in the offending cell.  
`GetRowErrors` extracts every such Error from an input table and returns a normalized table that is easy to load into data‑quality dashboards or refresh‑alerts.

---

## Syntax
```powerquery
(inputTable as table, 
 tableName as text, 
 indexColumn as text, 
 identifierColumn as text)
    as table
```

---

## Parameters

| Name | Type | Description |
|------|------|-------------|
| **inputTable** | table | The table to inspect for errors. |
| **tableName** | text | Friendly name copied to each output row—useful when you append logs from many tables. |
| **indexColumn** | text | Column that defines row order (e.g., an index). Renamed to **RowIndex**. |
| **identifierColumn** | text | Column that uniquely identifies the row (e.g., primary key). Renamed to **RowName**. |

---

## Returns
A table containing one row per error cell, with these columns:

| Column | Type | Description |
|--------|------|-------------|
| **TableName** | text | Value passed in **tableName**. |
| **RowIndex** | number | Original row index. |
| **RowName** | text | Original identifier value. |
| **ColumnName** | text | Name of the column that contained the error. |
| **Error.Reason** | text | High‑level error classification (e.g., *Type*). |
| **Error.Message** | text | Full error message from Power Query. |
| **Error.Detail** | text | Additional diagnostic details (often the offending value). |

---

## Processing Steps (high‑level)
1. Rename key columns (*indexColumn* → **RowIndex**, *identifierColumn* → **RowName**).  
2. Keep rows that contain at least one error.  
3. Add a column that stores the entire current row as a record and turn the record into a name/value table.  
4. Expand to cell level and keep only rows where **Value** is an error.  
5. Expand the error record into **Reason**, **Message**, **Detail**.  
6. Add **TableName**, select the final columns, and set data types.

---

## Complete Code (original solution)
```powerquery
(inputTable as table, tableName as text, indexColumn as text, identifierColumn as text) =>
let
    Source = inputTable,
    #"Renamed Index Column" = Table.RenameColumns(Source,{{indexColumn, "RowIndex"}}),
    #"Renamed Name Column" = Table.RenameColumns(#"Renamed Index Column",{{identifierColumn, "RowName"}}),
    #"Kept Errors" = Table.SelectRowsWithErrors( #"Renamed Name Column", Table.ColumnNames(#"Renamed Name Column")),
    #"Add Record Column" = Table.AddColumn(#"Kept Errors", "CURRENT ROW", each _),
    #"Added Custom" = Table.AddColumn(#"Add Record Column", "RECORD TO TABLE", each Record.ToTable([CURRENT ROW])),
    #"Expanded RECORD TO TABLE" = Table.ExpandTableColumn(#"Added Custom", "RECORD TO TABLE", {"Name", "Value"}, {"ColumnName", "Value"}),
    #"Kept Errors1" = Table.SelectRowsWithErrors(#"Expanded RECORD TO TABLE", {"Value"}),
    #"Added Column: CHECK ERRORS" = Table.AddColumn(#"Kept Errors1", "CHECK ERRORS", each try [Value]),
    #"Expanded CHECK ERRORS" = Table.ExpandRecordColumn(#"Added Column: CHECK ERRORS", "CHECK ERRORS", {"Error"}, {"Error"}),
    #"Expanded Error" = Table.ExpandRecordColumn(#"Expanded CHECK ERRORS", "Error", {"Reason", "Message", "Detail"}, {"Error.Reason", "Error.Message", "Error.Detail"}),
    #"Added Column: TableName" = Table.AddColumn(#"Expanded Error", "TableName", each tableName),
    #"Keep useful columns" = Table.SelectColumns(#"Added Column: TableName",{"TableName", "RowIndex", "RowName", "ColumnName", "Error.Reason", "Error.Message", "Error.Detail"}),
    #"Changed Type" = Table.TransformColumnTypes(#"Keep useful columns",{{"TableName", type text}, {"RowIndex", Int64.Type}, {"RowName", type text}, {"ColumnName", type text}, {"Error.Reason", type text}, {"Error.Message", type text}, {"Error.Detail", type text}})
in
    #"Changed Type"
```

---

## Example Usage
```powerquery
let
    // (Assume 'SalesRaw' is a query with an Index column and TransactionID)
    Source   = Excel.CurrentWorkbook(){[Name="SalesRaw"]}[Content],
    Changed  = Table.TransformColumnTypes(Source, {
                 {"TxnDate", type date},
                 {"Units", Int64.Type},
                 {"UnitPrice", type number}}),

    // Capture errors
    SalesErrors = GetRowErrors(
        inputTable       = Changed,
        tableName        = "SalesRaw",
        indexColumn      = "Index",
        identifierColumn = "TransactionID"
    )
in
    SalesErrors
```

---

## Future Improvements
* **Skip the first `Table.SelectRowsWithErrors`** and rely solely on the second pass to reduce scans on large tables.  
* **Combine the two record‑expansion steps** to avoid creating the transient *Error* column.  
* **Parameter validation** to raise a clear error if *indexColumn* or *identifierColumn* are missing.  
* **Return an empty table with the final schema** when no errors exist to ensure consistent downstream appends.  
* **Defensive rename logic** to guard against existing **RowIndex** or **RowName** columns.  
* **Explicit type coercion** for *RowIndex* to gracefully handle text index columns.

---

## Metadata
*Version:* 1.0  *Author:* <Your Name>  *Last Updated:* 2025-04-16
