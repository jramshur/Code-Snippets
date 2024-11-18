# Using GroupBy to concatanate row values into a single text string

## General Example
Using `Table.Group` to build a list of concatenated values for a given grouping
```
#"NewQueryName" = Table.Group(
    #"Source", 
    {"ColumnToGroupBy"}, 
    {{"NewColumnName", each Text.Combine([ColumnToCombine], "; "), type text}}
)
``` 

### Parameters

-   **#"Source"**: The source table that contains the data to be grouped.
-   **"ColumnToGroupBy"**: The name of the column used for grouping the rows.
-   **"NewColumnName"**: The name of the new column that will contain the concatenated text.
-   **"ColumnToCombine"**: The column whose values are to be concatenated for each group.

### Description

The `Table.Group` function groups the rows of the table based on the values in "ColumnToGroupBy". For each group, it combines the text from "ColumnToCombine" using the `Text.Combine` function, which concatenates the values with a semicolon separator. The result is a new table where each group is represented by a single row, and the concatenated texts are stored in "NewColumnName".


## Specific Example

Following is a specific and hypothetical scenario where we want to create a text string listing all order numbers for a given customer.

```
#"Grouped Rows" = Table.Group(
    #"Source", 
    {"Customer ID"}, 
    {{"CombinedComments", each Text.Combine(["Order Number"], ", "), type text}}
)
``` 

### Specific Parameters

-   **#"Source"**: This table from a previous step contains data about user comments.
-   **"Customer ID"**: The column used to group data by customer.
-   **"Combined Orders"**: A new column that will store all orders numbers of each customer, combined into a single text string.
-   **"Order Number"**: The original column containing order numbers to be concatenated. This is assuming a type text column. 

### Example Source Table
Example source table each order and customer. 

| Customer ID | Order Number|
|:---:|:---:|
| 101 | 101a|
| 101 | 101b|
| 101 | 101c|
| 102 | 102a|
| 102 | 102b|
| 103 | 103a|


### Example Output Table

The result of the operation is a table that summarizes all order numbers per customer into single rows separated by semicolons. 

|Customer ID|Combined Orders|
|:--:|:----|
| 101| 101a; 101b; 101c|
| 102| 102a; 102b|
| 103| 103a|
