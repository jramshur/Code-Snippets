# Title

## General Code Example
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

Following is a specific example with descriptive column names based on a hypothetical scenario where we group data by customer and combine comments:

m

Copy code

`#"Grouped Rows" = Table.Group(
    #"Source", 
    {"CustomerID"}, 
    {{"CombinedComments", each Text.Combine([Comments], ", "), type text}}
)` 

### Specific Parameters

-   **#"Source"**: This table from a previous step contains data about user comments.
-   **"CustomerID"**: The column used to group data by customer.
-   **"CombinedComments"**: A new column that will store all comments from each customer, combined into a single text string.
-   **"Comments"**: The original column containing textual comments to be concatenated.
