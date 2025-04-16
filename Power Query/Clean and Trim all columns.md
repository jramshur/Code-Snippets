
# Power Query Function: CleanTextColumns

## Purpose:
This function processes a given table by converting all columns to text, trimming leading and trailing spaces, and cleaning any unwanted characters from the text values.

## Input:
- **Source**: A table that contains the columns you want to clean.

## Output:
- A table with all columns converted to text, with extra spaces trimmed and unwanted characters cleaned.

## Function Code:

```m
(Source as table) as table =>
    let
        ColumnNames = Table.ColumnNames(Source),
        ConvertToText = List.Transform(ColumnNames, each {_, type text}),
        ChangedType = Table.TransformColumnTypes(Source, ConvertToText),
        TrimText = Table.TransformColumns(ChangedType, {}, Text.Trim),
        CleanText = Table.TransformColumns(TrimText, {}, Text.Clean)
    in
        CleanText
```

## Function Steps:
1. **Extract Column Names**:
   - `ColumnNames = Table.ColumnNames(Source)`
   - This step retrieves the names of all the columns in the input table `Source`.

2. **Convert Columns to Text**:
   - `ConvertToText = List.Transform(ColumnNames, each {_, type text})`
   - For each column in the table, the function transforms the data type to `text`.

3. **Change Column Types**:
   - `ChangedType = Table.TransformColumnTypes(Source, ConvertToText)`
   - This step applies the text type transformation to each column in the table.

4. **Trim Whitespace**:
   - `TrimText = Table.TransformColumns(ChangedType, {}, Text.Trim)`
   - Trims any leading and trailing spaces from the text values in all columns.

5. **Clean Text**:
   - `CleanText = Table.TransformColumns(TrimText, {}, Text.Clean)`
   - Removes any non-printable characters from the text in all columns.

## Example:
Given the following input table:

| Name      | Age    |
|-----------|--------|
|  John     |  25    |
|  Jane     |  30    |

After applying this function, the output table will look like:

| Name     | Age    |
|----------|--------|
| John     | 25     |
| Jane     | 30     |

## Usage Instructions:
1. Copy the code provided in the "Function Code" section.
2. Paste it into your Power Query editor as a custom function.
3. Pass your table as the `Source` parameter when calling the function.
4. The function will return a cleaned version of the table, with all columns in text format, with extra spaces trimmed, and unwanted characters cleaned.

## Future Improvements:
- Consider adding error handling for columns with null or invalid data types.
- Add an optional parameter to specify which columns to clean, instead of applying it to all columns.
- Allow users to select which types of cleaning operations to apply (e.g., trim only, clean only, or both).
