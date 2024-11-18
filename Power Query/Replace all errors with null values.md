 # Replacing All Error Values in a Table with Null

Power Query code to replace all error values in all columns with `null`.  Uses the `Table.ReplaceErrorValues` function along with `List.Transform` to achieve this dynamically for all columns.

## M Code
```m
    = Table.ReplaceErrorValues(Source, List.Transform(Table.ColumnNames(Source), each {_, null}))
```    

-   **List.Transform**: Applies a transformation to each item in `Table.ColumnNames`.
-   **each {_, null}**: For each column name, creates a list `{columnName, null}` indicating that errors should be replaced with `null`.


## Explanation
The expression `List.Transform(ColumnNames, each {_, null})` in Power Query is used to create a list of transformation rules for replacing error values in a table. Here’s a detailed breakdown:

1.  **`ColumnNames`**: This is a list of all column names in the table. For example, if your table has columns "Column1", "Column2", and "Column3", then `ColumnNames` would be `{"Column1", "Column2", "Column3"}`.
    
2.  **`List.Transform`**: This function applies a transformation to each item in a list. The syntax is `List.Transform(list, transformationFunction)`.
    
3.  **`each {_, null}`**: This part is the transformation function used by `List.Transform`. Here's what it does:
    
    -   **`each`**: This is a shorthand for an anonymous function in Power Query. It means "for each item in the list".
    -   **`{_, null}`**: This creates a two-element list where `_` represents the current item in the list being processed (in this case, a column name), and `null` is the value to replace errors with.

### Putting It All Together

-   **`List.Transform(ColumnNames, each {_, null})`**: For each column name in the list `ColumnNames`, create a two-element list `{columnName, null}`. This results in a list of lists, where each inner list represents a column and the value to replace errors with.

### Example

Let's say `ColumnNames` is `{"Column1", "Column2", "Column3"}`.

-   **Step-by-Step Transformation**:
    
    -   For "Column1": `{ "Column1", null }`
    -   For "Column2": `{ "Column2", null }`
    -   For "Column3": `{ "Column3", null }`
-   **Resulting List**: `{ {"Column1", null}, {"Column2", null}, {"Column3", null} }`
    

This resulting list is used by `Table.ReplaceErrorValues` to specify that errors in "Column1", "Column2", and "Column3" should all be replaced with `null`.
