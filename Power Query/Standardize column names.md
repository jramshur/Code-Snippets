## Column Name Standardization

This procedure is used to standardize the column names using Power Query. The aim is to ensure column names consist only of lowercase letters, numbers, and the greater-than symbol (">"). This standardization facilitates easier data manipulation and analysis by maintaining consistency and predictability in column naming conventions.

### Overview

The provided Power Query function cleans and formats the column names by:

1.  Removing non-printable characters.
2.  Trimming leading and trailing whitespace.
3.  Converting all letters to lowercase.
4.  Filtering out any characters that are not lowercase letters, numbers, or the ">" symbol.

### Example of standardization of column names

| **Original Column Name**          | **Standardized Column Name** |
|-----------------------------------|------------------------------|
| Name                              | name                         |
| E-mail Address                    | emailaddress                 |
| Date of Birth (YYYY/MM/DD)        | dateofbirthyyyymmdd          |
| Age (Years)                       | ageyears                     |
| Comments/Feedback                 | commentsfeedback             |
| Income [$]                        | income                       |
| Phone > Home > Mobile             | phone>home>mobile            |


## Power Query Function

Below is the Power Query M code that performs the aforementioned transformations:

```
= (Source as table) as table =>
    let
        ColName_clean = Table.TransformColumnNames(Source, Text.Clean), //optional
        ColName_trim = Table.TransformColumnNames(ColName_clean, Text.Trim), // optional
        ColName_lower = Table.TransformColumnNames(ColName_trim, Text.Lower),
        ColName_filtered = Table.TransformColumnNames(ColName_lower, each Text.Select(_, {"0".."9", "a".."z", ">"}))
    in 
        ColName_filtered
```

### Step-by-Step Explanation

1.  **Cleaning Column Names (`ColName_clean`)**:
    
    -   **Function Used**: `Text.Clean`
    -   **Purpose**: Removes all non-printable characters from the column names.
    -   **Example**: Converts `"Name\n"` to `"Name"`.
2.  **Trimming Column Names (`ColName_trim`)**:
    
    -   **Function Used**: `Text.Trim`
    -   **Purpose**: Trims leading and trailing whitespace from the column names cleaned in the previous step.
    -   **Example**: Converts `" Name "` to `"Name"`.
3.  **Lowercasing Column Names (`ColName_lower`)**:
    
    -   **Function Used**: `Text.Lower`
    -   **Purpose**: Converts all characters in the column names to lowercase for uniformity.
    -   **Example**: Converts `"Name"` to `"name"`.
4.  **Filtering Characters (`ColName_filtered`)**:
    
    -   **Function Used**: `Text.Select`
    -   **Purpose**: Retains only the characters specified (lowercase letters, numbers, and ">") in the column names.
    -   **Example**: Converts `"name-!@#"[>24]` to `"name>24"`.

### Usage of `Text.Select`

-   `Text.Select(_, {"0".."9", "a".."z", ">"})` effectively filters each column name to include only the specified characters. This function is crucial for aligning column names with technical and business standards that may dictate specific formatting rules.
