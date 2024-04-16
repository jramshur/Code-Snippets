// This code will convert each value in every column of your table to text format. The Text.From(_, "en-US") function is used to convert each value to text, ensuring that numbers are formatted correctly according to the English (United States) locale. Adjust the locale if needed based on your data.
// You can replace "SourceTable" with the actual name of your table. This code assumes that all columns need to be transformed. If you want to apply this transformation to only specific columns, you can adjust the Table.ColumnNames(Source) part to specify the columns you want to transform.

let
    // Assuming your original table is named "SourceTable"
    Source = SourceTable,
    // Transform each column to text
    TransformEachColumn = Table.TransformColumns(
        Source,
        // Transform each column
        List.Transform(
            Table.ColumnNames(Source),
            each {_, each Text.From(_, "en-US")}
        )
    )
in
    TransformEachColumn
