import pandas as pd
import numpy as np

df = pd.read_csv('quosaexport.csv')

df = pd.read_csv("data.csv",index_col='MyColumn')

# Write DataFrame into CSV
df.to_csv("data-out.csv")

## Filter/Select rows by position
# select the first 2 rows
df.iloc[:2]
# select the last 2 rows
df.iloc[-2:]

## Filter/Select Rows by index value
#select rows up to and including the one
# with index=2 (this retrieves 3 rows)
df.loc[:2]

## Filter/select rows by column value
# people whose "age" is greater than 30
df[df["age"] > 30]
# people who have more pets than children
df[ df["num_pets"] > df[ "num_children"] ]

## Filter/select rows by multiple column valuesPermalink
# people older than 40 who own pets
df[ (df["age"] > 40) & (df["num_pets"] > 0) ] 

## drop a column
# df itself is not modified; a copy is returned instead
df.drop(["age","num_children"],axis=1)

## Drop duplicated rows based on a column's value
duplicated_titles = movies_df.duplicated(subset=['title'], keep=False)
# tilde is used to to dataframe subraction!
movies_df = movies_df[~duplicated_titles]

## Apply an aggregate function to every column
df[["age","num_pets","num_children"]].apply(lambda row: np.mean(row),axis=0)

## Apply an aggregate function to every row
df[["age","num_pets","num_children"]].apply(lambda row: np.sum(row),axis=1)


## Add a new column based on a another one
df["pets_and_children"] = df["num_pets"] + df["num_children"]
df["name_uppercase"] = df[["name"]].apply(lambda name: name.str.upper())

## To select rows whose column value equals a scalar, some_value, use ==:
df.loc[df['column_name'] == some_value]
df.loc[df['column_name'] != some_value]
# To select rows whose column value is in an iterable, some_values, use isin:
df.loc[df['column_name'].isin(some_values)]
# Combine multiple conditions with &:
df.loc[(df['column_name'] == some_value) & df['other_column'].isin(some_values)]
# isin returns a boolean Series, so to select rows whose value is not in some_values, negate the boolean Series using ~:
df.loc[~df['column_name'].isin(some_values)]


## Rename column
df.rename(columns={'oldName1': 'newName1', 'oldName2': 'newName2'}, inplace=True)

Size of DF
# Use the `shape` property
print(df.shape)
# Or use the `len()` function with the `index` property
print(len(df.index))
