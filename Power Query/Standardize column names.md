## Column Name Standardization

## Overview

This Power Query function standardizes column names in a dataset to ensure they are consistent and easy to work with. The function performs the following transformations:

1. Removes non-printable characters.
2. Trims leading and trailing whitespace.
3. Converts all characters to lowercase.
4. Retains only specific characters: lowercase letters (`a-z`), numbers (`0-9`), and the greater-than symbol (`>`).

These transformations help enforce uniform naming conventions, reducing the likelihood of errors during data processing.


## Power Query Function Code

```powerquery
= (Source as table) as table =>
    let
        ColName_clean = Table.TransformColumnNames(Source, Text.Clean), // optional
        ColName_trim = Table.TransformColumnNames(ColName_clean, Text.Trim), // optional
        ColName_lower = Table.TransformColumnNames(ColName_trim, Text.Lower),
        ColName_filtered = Table.TransformColumnNames(ColName_lower, each Text.Select(_, {"0".."9", "a".."z", ">"}))
    in 
        ColName_filtered
```

## Key Changes in Column Names

1. **Removed Non-Printable Characters**:

2. **Trimmed Leading/Trailing Whitespace**:
   - `" Name "` → `"name"`

3. **Converted to Lowercase**:
   - `"E-mail Address"` → `"emailaddress"`

4. **Retained Only Allowed Characters**:
   - `"Date of Birth (YYYY/MM/DD)"` → `"dateofbirthyyyymmdd"`
   - `"Age (Years)"` → `"ageyears"`
   - `"Income [$]"` → `"income"`

5. **Preserved the Greater-Than Symbol (`>`)**:
   - `"Phone > Home > Mobile"` → `"phone>home>mobile"`
   - Keeping the '>' was useful for my use case. It may not be useful for all use cases. 


## Example of column transformations

| **Original Column Name**          | **Standardized Column Name** |
|-----------------------------------|------------------------------|
| Name                              | name                         |
| E-mail Address                    | emailaddress                 |
| Date of Birth (YYYY/MM/DD)        | dateofbirthyyyymmdd          |
| Age (Years)                       | ageyears                     |
| Comments/Feedback                 | commentsfeedback             |
| Income [$]                        | income                       |
| Phone > Home > Mobile             | phone>home>mobile            |


## Purpose and Benefits

This function simplifies and standardizes column names, ensuring:

- Consistency across datasets.
- Easier integration and manipulation in tools like Power BI.
- Elimination of potential errors caused by special characters or inconsistent naming conventions.

Using this function ensures that your datasets are prepared for seamless processing and analysis.
