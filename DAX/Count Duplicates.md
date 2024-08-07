# Counting Duplicates in a Filtered Table Using DAX

This document presents two DAX measures to count the number of duplicate values in a column after applying a filter to another column. Both solutions use the `SUMMARIZE` function to aggregate data and the `FILTER` function to identify duplicates.

## Solution 1: Condensed Solution

### DAX Measure

```DAX
VAR dupcount =
    COUNTROWS(
        FILTER(
            SUMMARIZE(
                FILTER(
                    YourTableName,
                    YourTableName[FilterColumn] = "FilterValue"
                ),
                YourTableName[ColumnName],
                "Count", COUNT(YourTableName[ColumnName])
            ),
            [Count] > 1
        )
    )
VAR output = IF(ISBLANK(dupcount), 0, dupcount)

RETURN output
```

### Explanation

1.  **FilteredTable**: Filters `YourTableName` to include only rows where `FilterColumn` equals `"FilterValue"`.
2.  **SummarizedTable**: Uses `SUMMARIZE` to aggregate `FilteredTable` by `ColumnName` and counts the occurrences of each value.
3.  **Duplicates**: Uses `FILTER` to identify rows in `SummarizedTable` where the count of `ColumnName` values is greater than 1.
4.  **dupcount**: Counts the rows in the `Duplicates` table.
5.  **output**: Returns `dupcount` if it is not blank, otherwise returns 0.

## Solution 2: Refined Solution

### DAX Measure

```DAX
`Count of Duplicates with Filter = 
VAR FilteredTable =
    FILTER(
        YourTableName,
        YourTableName[FilterColumn] = "FilterValue"
    )
VAR SummarizedTable =
    SUMMARIZE(
        FilteredTable,
        YourTableName[ColumnName],
        "Count", COUNT(YourTableName[ColumnName])
    )
VAR Duplicates =
    FILTER(
        SummarizedTable,
        [Count] > 1
    )
VAR dupcount = COUNTROWS(Duplicates)
RETURN IF(ISBLANK(dupcount), 0, dupcount)` 
```
### Explanation

1.  **FilteredTable**: Filters `YourTableName` to include only rows where `FilterColumn` equals `"FilterValue"`.
2.  **SummarizedTable**: Summarizes the filtered table by `ColumnName` and counts the occurrences of each value.
3.  **Duplicates**: Filters the summarized table to only include values that appear more than once.
4.  **dupcount**: Counts the rows in the `Duplicates` table.
5.  **RETURN**: Returns the count of duplicates, ensuring it returns 0 instead of a blank.

## Conclusion

Both solutions effectively count the number of duplicate values in a column after filtering the table based on another column. The refined solution organizes the steps into a clearer structure, but both achieve the same result.
