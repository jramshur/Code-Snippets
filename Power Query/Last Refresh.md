# Last Refresh Time for Datasets and Dataflows
This Power Query code creates a table to track the last refresh date of datasets and dataflows in both UTC (Coordinated Universal Time) and CST (Central Standard Time).

``` powerquery
let
  Source = #table({"Last Refresh (UTC)", "Last Refresh (CST)"}, {{DateTimeZone.UtcNow(), DateTimeZone.SwitchZone(DateTimeZone.UtcNow(), -6)}}),
  #"Changed column type" = Table.TransformColumnTypes(Source, {{"Last Refresh (UTC)", type datetimezone}, {"Last Refresh (CST)", type datetimezone}})
in
  #"Changed column type"
```

### Explanation
1. **Create a Table with UTC and CST Times**:
   - The `Source` step creates a table with two columns:
     - **Last Refresh (UTC)**: Displays the current UTC time using `DateTimeZone.UtcNow()`.
     - **Last Refresh (CST)**: Converts the UTC time to CST by applying a time zone offset of -6 hours with `DateTimeZone.SwitchZone(DateTimeZone.UtcNow(), -6)`.

2. **Change Column Types**:
   - The `#"Changed column type"` step ensures both columns are explicitly defined as `datetimezone` types, maintaining consistency for time zone-aware datetime values.

### Example Output

- The final table contains:
     - UTC time of the last refresh.
     - CST time of the last refresh.

| Last Refresh (UTC) | Last Refresh (CST)|
|:---:|:---:|
| 2024-12-11T15:00:00.000Z | 2024-12-11T09:00:00.000-06:00|
