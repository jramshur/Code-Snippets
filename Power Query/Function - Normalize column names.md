## Power Query Column Name Standardization

This document outlines the procedure to standardize the column names of a table in Power Query. The aim is to ensure column names consist only of lowercase letters, numbers, and the greater-than symbol (">"). This standardization facilitates easier data manipulation and analysis by maintaining consistency and predictability in column naming conventions.

### Overview

The provided Power Query function cleans and formats the column names by:

1.  Removing non-printable characters.
2.  Trimming leading and trailing whitespace.
3.  Converting all letters to lowercase.
4.  Filtering out any characters that are not lowercase letters, numbers, or the ">" symbol.

### Power Query Function

Below is the Power Query M code that performs the aforementioned transformations:

```
= (Source as table) as table =>
    let
        ColName_clean = Table.TransformColumnNames(Source, Text.Clean), //optional
        ColName_trim = Table.TransformColumnNames(ColName_clean, Text.Trim), // optional
        ColName_lower = Table.TransformColumnNames(ColName_trim, Text.Lower),
        ColName_filtered = Table.TransformColumnNames(ColName_lower, each Text.Select(_, "abcdefghijklmnopqrstuvwxyz0123456789>"))
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

-   `Text.Select(_, "abcdefghijklmnopqrstuvwxyz0123456789>")` effectively filters each column name to include only the specified characters. This function is crucial for aligning column names with technical and business standards that may dictate specific formatting rules.

### Conclusion

The function simplifies the process of cleaning and standardizing column names, making the data set more structured and easier to work with in Power BI and other data processing tools. This standardization is particularly useful in scenarios involving data integration from multiple sources, ensuring that column names do not cause errors in data processing scripts or queries due to inconsistent naming conventions.
