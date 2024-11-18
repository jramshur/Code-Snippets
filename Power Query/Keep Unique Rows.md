
# **Keep Unique Values in Power Query**

This guide demonstrates how to identify and keep unique rows in a dataset using Power Query. The approach involves isolating duplicate values and removing them, leaving only the unique rows in the final output.

---

## **Code Overview**

This script isolates duplicates based on specified columns and removes them, keeping only unique rows.

```powerquery
let 
    columnNames = {"Column1"}, 
    addCount = Table.Group(#"Previous Step Name", columnNames, {{"Count", Table.RowCount, type number}}), 
    selectDuplicates = Table.SelectRows(addCount, each [Count] > 1), 
    removeCount = Table.RemoveColumns(selectDuplicates, "Count") 
in 
    Table.Join(#"Previous Step Name", columnNames, removeCount, columnNames, JoinKind.Inner)
```

---

## **Steps Breakdown**

### 1. Define Columns for Duplicate Detection
```powerquery
columnNames = {"Column1"}
```
- Specifies the column(s) for identifying duplicates.
- Replace `"Column1"` with the name(s) of the column(s) relevant to your dataset.

---

### 2. Group Rows and Count Occurrences
```powerquery
addCount = Table.Group(#"Previous Step Name", columnNames, {{"Count", Table.RowCount, type number}})
```
- Groups data by the specified column(s) and adds a `Count` column that tracks how many times each group occurs.

---

### 3. Filter Out Duplicates
```powerquery
selectDuplicates = Table.SelectRows(addCount, each [Count] > 1)
```
- Filters the grouped data to retain only rows where the `Count` column is greater than 1, identifying duplicate groups.

---

### 4. Remove Count Column
```powerquery
removeCount = Table.RemoveColumns(selectDuplicates, "Count")
```
- Removes the `Count` column, leaving only the duplicate groups.

---

### 5. Join Back to Original Dataset
```powerquery
Table.Join(#"Previous Step Name", columnNames, removeCount, columnNames, JoinKind.Inner)
```
- Performs an inner join with the original dataset using the specified column(s), resulting in a table of unique rows.

---

## **Function Version**

Here’s a reusable function that implements the above logic:

```powerquery
// Function to Keep Unique Values
let
    KeepUniqueValues = (inputTable as table, columnNames as list) as table =>
    let
        addCount = Table.Group(inputTable, columnNames, {{"Count", Table.RowCount, type number}}),
        selectDuplicates = Table.SelectRows(addCount, each [Count] > 1),
        removeCount = Table.RemoveColumns(selectDuplicates, "Count"),
        result = Table.Join(inputTable, columnNames, removeCount, columnNames, JoinKind.Inner)
    in
        result
in
    KeepUniqueValues
```

### **Function Parameters**
- `inputTable`: The table to process.
- `columnNames`: A list of column names to check for duplicates.

### **How to Use the Function**
1. Call the `KeepUniqueValues` function in your query.
2. Provide the input table and column(s) for duplicate detection.

Example:
```powerquery
let
    UniqueRows = KeepUniqueValues(#"Previous Step Name", {"Column1"})
in
    UniqueRows
```

---

## **Source Reference**
Inspired by the blog post: [A Twist to Turn Keep Duplicates into Keep Unique in Power Query](https://wmfexcel.com/2022/04/07/a-twist-to-turn-keep-duplicates-into-keep-unique-in-powerquery/).

---
