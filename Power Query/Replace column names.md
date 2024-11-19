
# Replace Column Names using a mapping table

## Purpose
This Power Query script contains a solution for renaming columns in a table using a mapping table and the `Table.RenameColumns` function.

---

## Approach 1: Step-by-Step Column Renaming

This approach outlines the steps to rename columns using a mapping table.

### Code
```powerquery
let
    // Load the mapping table containing old and new column names
    Source = tblWithNameMapping,
    
    // Select the relevant columns from the mapping table
    Mapping = Table.SelectColumns(Source, {"Old_ColumnName", "New_ColumnName"}),
    
    // Convert the mapping table into a list of lists for Table.RenameColumns
    MappingList = Table.ToRows(Mapping),
    
    // Rename columns in the data table (tblData) using the mapping list
    #"Rename all columns" = Table.RenameColumns(tblData, MappingList)
in
    #"Rename all columns"
```

### Steps
1. **Load the Mapping Table**: The mapping table (`tblWithNameMapping`) contains two columns: `Old_ColumnName` and `New_ColumnName`.
2. **Select Relevant Columns**: Only the `Old_ColumnName` and `New_ColumnName` columns are used.
3. **Convert Table to List**: The mapping table is converted into a list of lists format required by `Table.RenameColumns`.
4. **Rename Columns**: The `Table.RenameColumns` function is applied to the target table (`tblData`) using the mapping list.

---

## Approach 2: Reusable Function

This approach defines a reusable function to rename columns in any table using a mapping table.

### Code
```powerquery
// Function to rename columns in a table based on a mapping table
(renameColumns) =>
let
    renameColumnsTable = (tableToRename as table, columnMappingTable as table) =>
    let
        // List of old column names
        oldColumnNames = Table.ColumnNames(tableToRename),
        
        // List of new column names based on mapping table
        newColumnNames = List.Transform(oldColumnNames, 
            each try Table.SelectRows(columnMappingTable, each [Old_ColumnName] = _) otherwise _),
        
        // Rename columns using old and new column names
        renamedTable = Table.RenameColumns(tableToRename, List.Zip({oldColumnNames, newColumnNames}))
    in
        renamedTable,

    // Invoke the inner function with the provided inputs
    result = renameColumnsTable(renameColumns{0}, renameColumns{1})
in
    result
```

### Usage
```powerquery
// Invoke the function with the data table and column mapping table
renamedTable = renameColumns({dataTable, columnMappingTable})
```

### Steps
1. **Define Function**: A reusable function `renameColumns` is defined to accept:
   - `tableToRename`: The table whose columns will be renamed.
   - `columnMappingTable`: The mapping table containing `Old_ColumnName` and `New_ColumnName`.
2. **Extract Column Names**: The function identifies the old column names and matches them with their new names using the mapping table.
3. **Rename Columns**: The function applies the `Table.RenameColumns` method with the old and new column names zipped together.
4. **Invoke the Function**: Pass the data table and mapping table as arguments to the function.

---

## Key Concepts
- **Mapping Table**: Contains two columns:
  - `Old_ColumnName`: The current column names in the table.
  - `New_ColumnName`: The desired column names after renaming.
- **`Table.RenameColumns`**: Requires a list of `{old_name, new_name}` pairs to rename columns in a table.

---

## Advantages
1. **Approach 1**: Simple and straightforward for specific use cases where renaming logic is static.
2. **Approach 2**: Reusable for dynamic scenarios involving multiple tables or varying column names.

---

## Dependencies
- Power Query/M language
- Mapping table with correct column names (`Old_ColumnName`, `New_ColumnName`)
