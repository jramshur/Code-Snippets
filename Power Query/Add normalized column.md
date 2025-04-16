
# Add normalized column Function Documentation

## Summary
The `fxn_AddNormalizedColumn` function adds a new column to a table by duplicating a specified existing column, with an option to normalize its content. Normalization involves transforming text to lowercase and selectively retaining characters.

## Syntax
```
fxn_AddNormalizedColumn(table as table, columnName as text, newColumnName as text, allowedCharacters as any, optional flagLowerCase as logical) as table
```

## Parameters

- **table (required)**: The input table.
- **columnName (required)**: The name of the column to duplicate and normalize.
- **newColumnName (required)**: The name of the new column to add to the table.
- **allowedCharacters (required)**: Specifies which characters are allowed in the normalized text. This can be:
  - A custom list of characters to retain.
  - A preset string defining common character sets:
    - `"Alphanumeric"`: Allows digits (0-9) and letters (A-Z, a-z).
    - `"AlphanumericLowercase"`: Allows digits (0-9) and lowercase letters (a-z).
    - `"AlphanumericWithSymbols"`: Allows digits, lowercase letters, and symbols (-, _, .).
    - `"LettersOnly"`: Allows uppercase and lowercase letters (A-Z, a-z).
    - `"DigitsOnly"`: Allows digits (0-9).
- **flagLowerCase (optional)**: If `true`, converts the text to lowercase before retaining the allowed characters.

## Detailed Steps
1. **Column Duplication**: The function duplicates the specified column from the input table.
2. **Character Selection**: Using the `allowedCharacters` parameter, the function filters the duplicated column to retain only the specified characters.
3. **Case Conversion**: If `flagLowerCase` is `true`, the text in the duplicated column is first converted to lowercase before applying the allowed characters.

## Full Code

```m
(table as table, columnName as text, newColumnName as text, allowedCharacters as any, optional flagLowerCase as logical) as table =>
    let
        // Define preset character sets
        presetCharacterSets = [
            Alphanumeric = {"0".."9", "a".."z", "A".."Z"},
            AlphanumericLowercase = {"0".."9", "a".."z"},
            AlphanumericWithSymbols = {"0".."9", "a".."z", ".", "-", "_"},
            LettersOnly = {"a".."z", "A".."Z"},
            DigitsOnly = {"0".."9"}
        ],

        // If allowedCharacters is set to "preset", choose a preset set
        finalAllowedCharacters = 
            if allowedCharacters = "Alphanumeric" then presetCharacterSets[Alphanumeric] 
            else if allowedCharacters = "AlphanumericLowercase" then presetCharacterSets[AlphanumericLowercase]
            else if allowedCharacters = "AlphanumericWithSymbols" then presetCharacterSets[AlphanumericWithSymbols]
            else if allowedCharacters = "LettersOnly" then presetCharacterSets[LettersOnly]
            else if allowedCharacters = "DigitsOnly" then presetCharacterSets[DigitsOnly]
            else allowedCharacters,  // Otherwise use custom list of characters

        // Ensure the specified column exists in the table
        ColumnExists = List.Contains(Table.ColumnNames(table), columnName),
        Result = if ColumnExists then
            let
                // Duplicate the specified column
                DuplicatedColumn = Table.AddColumn(table, newColumnName, each Record.Field(_, columnName)),

                // Apply case conversion if specified
                TransformedColumn = if flagLowerCase = null or flagLowerCase = false 
                    then Table.TransformColumns(DuplicatedColumn, {{newColumnName, each Text.Select(_, finalAllowedCharacters), type text}})
                    else Table.TransformColumns(DuplicatedColumn, {{newColumnName, each Text.Select(Text.Lower(_), finalAllowedCharacters), type text}})
            in
                TransformedColumn
        else
            error "The specified column does not exist in the table."
    in
        Result
```

## Example Usage

1. **Using a preset (`AlphanumericLowercase`)**:
    ```m
    #"Add CFN_normalized column" = fxn_AddNormalizedColumn(#"Trim and clean all columns", PARTCODE_ColumnName, "CFN_norm", "AlphanumericLowercase", true)
    ```

2. **Using a custom character set**:
    ```m
    #"Add CFN_normalized column" = fxn_AddNormalizedColumn(#"Trim and clean all columns", PARTCODE_ColumnName, "CFN_norm", {"0".."9", "a".."z", ".", "-", "_"}, true)
    ```

3. **Using another preset (`LettersOnly`)**:
    ```m
    #"Add CFN_normalized column" = fxn_AddNormalizedColumn(#"Trim and clean all columns", PARTCODE_ColumnName, "CFN_norm", "LettersOnly", false)
    ```
