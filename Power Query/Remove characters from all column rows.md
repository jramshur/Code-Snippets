  
# Remove/Keep characters in column rows

This document outlines various methods to clean text data in Power Query by removing unwanted characters or keeping only wanted characters from a column. We will cover three main approaches. Also provided is a useful table of ASCII character ranges.


## ASCII Character Ranges for Text Cleaning in Power Query

Below is an overview of useful ASCII character ranges that are commonly used in text cleaning processes within Power Query. These can be used to either include or exclude specific types of characters using functions like `Text.Select` and `Text.Remove`.

#### Table of ASCII Character Ranges

| Category | From | To | Characters Included | Common Use |
|:-------|------|----|---------------------|------------|
| **Control Characters**  | 0 | 31 | (various control characters) | Usually removed from text data |
| **Space**                  | 32   | 32 | (space) | Keeping spaces if needed |
| **Basic Punctuation**  | 33   | 47 | ! " # $ % & ' ( ) * + , - . / | Removing/keeping basic punctuation |
| **Numbers**                | 48 | 57 | 0-9 | Keeping digits  |
| **Colon/Semicolon**  | 58   | 59 | : ; | Removing/keeping colons and semicolons |
| **Comparison & Math Symbols**| 60 | 64 | < = > ? @ | Removing/keeping mathematical and comparison symbols|
| **Uppercase Letters**      | 65 | 90 | A-Z | Keeping uppercase letters |
| **Brackets**          | 91   | 96 | [ \ ] ^ _ ` | Removing/keeping various brackets and caret |
| **Lowercase Letters**      | 97   | 122| a-z | Keeping lowercase letters |
| **Curly Braces & Pipe**    | 123  | 125| { \| } | Removing/keeping curly braces and pipe|
| **Extended Punctuation**   | 126  | 126| ~ | Removing/keeping tilde |

### Useful list of ranges and list of characters

- Alphanumeric Characters and Spaces `{"0".."9", "a".."z", "A".."Z", " "}`
- Basic Punctuation `{"!".."/"}` 
- `{"(", ")", "[", "]", "{", "}", " ", "-", "/", "\", "|", "#", "&", "*", ".", "," , ";", ":", "<", ">", "?", "^", "%", "$", "@", "!", "~", "=", "+"}`


## 1. Using `Text.Select` to Keep Certain Characters

The `Text.Select` function is used to specify which characters to retain in the text, effectively removing all others.

### Code Example

```
let
    Source = YourDataSource, // Replace with your data source
    CleanedTable = Table.TransformColumns(Source, {
        {"Column1", each Text.Select(_, {"0".."9", "a".."z", "A".."Z"}), type text}
    })
in
    CleanedTable
```
### Explanation

-   **Text.Select** function keeps only the characters specified in the list `{"0".."9", "a".."z", "A".."Z"}`, which includes all lowercase letters, uppercase letters, and digits.
-   This transformation is applied to `Column1`.
-   Removes all non-alphanumeric characters (punctuation, symbols, whitespace, etc.).

## 2. Using `Text.Remove` to Remove All Characters Except Alphanumeric

This method defines a list of characters that should be removed by determining the complement set of alphanumeric characters.

### Code Example

```
let
    Source = YourDataSource, // Replace with your data source
    
    // Define characters to keep list
    CharactersToKeep = List.Transform({48..57, 65..90, 97..122}, each Character.FromNumber(_)),
    
    // Define all printable ASCII characters list
    AllCharacters = List.Transform({32..126}, each Character.FromNumber(_)),
    
    // Calculate characters to remove (set difference)
    CharactersToRemove = List.Difference(AllCharacters, CharactersToKeep),
    RemoveString = Text.Combine(CharactersToRemove, ""),
    
    // Transform the specified column
    CleanedTable = Table.TransformColumns(Source, {
        {"Column1", each Text.Remove(_, RemoveString), type text}
    })
in
    CleanedTable
```

### Explanation

-   **CharactersToKeep** contains all alphanumeric characters.
-   **AllCharacters** contains all printable ASCII characters.
-   **CharactersToRemove** is calculated using the set difference, which finds all characters not in the `CharactersToKeep` list.
-   **Text.Remove** is used to strip out all characters identified in `CharactersToRemove`.

## 3. Using `Text.Remove` Directly to Define Removal Set

In this approach, `Text.Remove` is directly used with a manually defined list of characters to remove.

### Code Example

```
let
    Source = YourDataSource, // Replace with your data source
    CleanedTable = Table.TransformColumns(Source, {
        {"Column1", each Text.Remove(_, {"a", "b", "c"}), type text}
    })
in
    CleanedTable
```

### Explanation

-   Directly specifies the characters to remove: `{"a", "b", "c"}`.
-   This list can be customized to include any characters you wish to exclude from `Column1`.
-   Useful for targeted removals and simpler scenarios.

# Conclusion

These methods provide flexible approaches to cleaning text data in Power Query, whether you need to keep only certain characters or remove specific unwanted characters. Each method can be tailored to the specific requirements of your data cleaning task.
