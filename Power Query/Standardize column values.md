# Normalize Column Values

`Create Normalized Column` is a Power Query function that duplicates a specified column in a table and transforms the duplicated column to retain only specified characters. This function also allows optional case transformation to lowercase.

## Function Definition

```powerquery
(table as table, columnName as text, newColumnName as text, allowedCharacters as list, optional toLower as logical) as table =>
    let
        // Duplicate the specified column
        DuplicatedColumn = Table.AddColumn(table, newColumnName, each Record.Field(_, columnName)),
        // Apply case conversion if specified
        TransformedColumn = if toLower = true 
            then Table.TransformColumns(DuplicatedColumn, {{newColumnName, each Text.Select(Text.Lower(_), allowedCharacters), type text}})
            else Table.TransformColumns(DuplicatedColumn, {{newColumnName, each Text.Select(_, allowedCharacters), type text}})
    in
        TransformedColumn
```

## Parameters

-   **`table`**: _(table)_  
    The input table containing the column to duplicate and normalize.
    
-   **`columnName`**: _(text)_  
    The name of the column to duplicate.
    
-   **`newColumnName`**: _(text)_  
    The name of the new duplicated and normalized column.
    
-   **`allowedCharacters`**: _(list)_  
    A list of characters to retain in the normalized column. For example, `{"0".."9", "A".."Z", "a".."z"}` will keep only alphanumeric characters.
    
-   **`optional toLower`**: _(logical)_  
    An optional parameter to specify case transformation:
    
    -   **`true`**: Convert all characters in the new column to lowercase.
    -   **`false`** or **unspecified**: Keep the original case.

## Usage Example

The following example demonstrates how to use the `Create_Normalized_Column` function:

```powerquery
// Define the allowed characters to keep (alphanumeric)
let
    Source = /* Your data source */,
    Result = Create_Normalized_Column(Source, "OriginalColumnName", "NormalizedColumn", {"0".."9", "A".."Z", "a".."z"}, true)
in
    Result
```
In this example:

-   The column `"OriginalColumnName"` is duplicated.
-   The new column is named `"NormalizedColumn"`.
-   Only alphanumeric characters are kept.
-   All characters are transformed to lowercase.

## Useful `allowedCharacters` list
Here are some useful `allowedCharacters` lists you might consider for various data-cleaning needs:

 1. **Alphanumeric Characters**
	-   Keeps only letters (A-Z, a-z) and numbers (0-9).
	-   Commonly used to remove special characters and punctuation.
	`{"0".."9", "A".."Z", "a".."z"}` 
	`{"0".."9", "a".."z"}` 

2. **Alphabetic Characters Only**
	-   Keeps only letters, removing any numbers or special characters.
	`{"A".."Z", "a".."z"}` 

3. **Numeric Characters Only**
	-   Keeps only numbers. Useful for extracting numeric data from mixed text.
	`{"0".."9"}` 

4. **Alphanumeric with Basic Punctuation**
	-   Keeps letters, numbers, and a few common punctuation marks like periods and hyphens. Useful for addresses, product codes, etc.
	`{"0".."9", "A".."Z", "a".."z", ".", "-", "_"}` 

5. **Hexadecimal Characters**
	-   Keeps characters that appear in hexadecimal values (0-9 and A-F). Useful for processing IDs, color codes, etc.
	`{"0".."9", "A".."F", "a".."f"}` 

6. **Currency Symbols and Numeric Characters**
	-   Keeps numbers and some common currency symbols. Useful for financial data. 
	- `{"0".."9", "$", "€", "£", "¥"}` 

7. **Whitespace and Alphanumeric**
	-   Keeps letters, numbers, and whitespace. Useful for basic text normalization while preserving spaces.
	`{"0".."9", "A".."Z", "a".."z", " "}` 

 8. **URL-Safe Characters**
	-   Keeps characters commonly used in URLs and filenames (letters, numbers, hyphens, underscores, and periods).
	`{"0".."9", "A".."Z", "a".."z", "-", "_", "."}` 

## Notes

-   **Character Selection**: The `allowedCharacters` parameter provides flexibility to specify exactly which characters to keep in the duplicated column.
-   **Case Transformation**: The `toLower` parameter is optional, allowing case sensitivity as required.

## Purpose

This function is useful for:

-   Normalizing text data to a standard format.
-   Ensuring only specific characters (e.g., alphanumeric) are retained in a dataset.
-   Simplifying column transformations in Power Query.

## Additional Considerations

If additional case transformations are required, such as uppercase, the function could be further customized by adding a parameter to specify case options (e.g., "none", "lower", "upper").


