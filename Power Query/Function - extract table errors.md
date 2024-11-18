# Extract Errors from a Table

## Description

This Power Query function extracts rows containing errors from a specified table, transforms and annotates the data for easier error identification and analysis.

## Parameters
- **inputTable** (table): The source table from which errors will be extracted.
- **tableName** (text): Text to display in the `TableName` column to indicate the source table of the errors when appending error tables.
- **indexColumn** (text): The name of the index/ID column in the input table.
- **identifierColumn** (text): The name of a column in the table used to help identify errors in the resulting table. The combination of `indexColumn` and `identifierColumn` will help trace the errors.


## Function Steps

1. **Source**: Initialize the function with the input parameters.
2. **Rename Columns**:
   - Rename the `indexColumn` to `RowIndex`.
   - Rename the `identifierColumn` to `RowName`.
3. **Select Rows with Errors**: Filter the table to keep only the rows that contain errors.
4. **Add Record Column**: Add a column named `CURRENT ROW` which contains the entire row as a record.
5. **Convert Record to Table**: Add a column named `RECORD TO TABLE` which converts each row record to a table.
6. **Expand Table Column**: Expand the `RECORD TO TABLE` column to separate `ColumnName` and `Value`.
7. **Select Rows with Errors (Value)**: Filter the table again to keep only rows where the `Value` column contains errors.
8. **Check Errors**: Add a column named `CHECK ERRORS` which attempts to access the `Value` column.
9. **Expand Error Column**: Expand the `CHECK ERRORS` column to include `Error.Reason`, `Error.Message`, and `Error.Detail`.
10. **Add TableName Column**: Add a column named `TableName` to include the `tableName` value.
11. **Select Useful Columns**: Select only the relevant columns for the final output: `TableName`, `RowIndex`, `RowName`, `ColumnName`, `Error.Reason`, `Error.Message`, `Error.Detail`.
12. **Change Column Types**: Ensure the column types are correctly set:
    - `TableName` as text.
    - `RowIndex` as Int64.
    - `RowName`, `ColumnName`, `Error.Reason`, `Error.Message`, and `Error.Detail` as text.


## Code


```
let
    ExtractErrors = (inputTable as table, tableName as text, indexColumn as text, identifierColumn as text) => let
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
in
    ExtractErrors
```

## Example

### Input Table (`SampleTable`):

| ID  | Name    | Value  |
|-----|---------|--------|
| 1   | Alpha   | 10     |
| 2   | Beta    | Error  |
| 3   | Gamma   | 30     |
| 4   | Delta   | Error  |
| 5   | Epsilon | 50     |

### Function Call:

```
let
    SampleTable = Table.FromRecords({
        [ID = 1, Name = "Alpha", Value = 10],
        [ID = 2, Name = "Beta", Value = Error.Record("Type", "Expression.Error", "Message", "An error occurred.")],
        [ID = 3, Name = "Gamma", Value = 30],
        [ID = 4, Name = "Delta", Value = Error.Record("Type", "Expression.Error", "Message", "Another error occurred.")],
        [ID = 5, Name = "Epsilon", Value = 50]
    }),
    ErrorTable = ExtractErrors(SampleTable, "SampleTable", "ID", "Name")
in
    ErrorTable
```

### Output Table (`ErrorTable`):

| TableName  | RowIndex | RowName | ColumnName | Error.Reason     | Error.Message           | Error.Detail |
|------------|----------|---------|------------|------------------|-------------------------|--------------|
| SampleTable| 2        | Beta    | Value      | Expression.Error | An error occurred.      | (details)    |
| SampleTable| 4        | Delta   | Value      | Expression.Error | Another error occurred. | (details)    |
