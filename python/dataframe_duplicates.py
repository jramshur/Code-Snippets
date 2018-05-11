import pandas as pd

myfile="C:\\myfilepath\\myexcelfile.xlsx"
df = pd.read_excel(open(myfile,'rb'), sheet_name="mysheetname")

# return series containing all duplicates
df[df.duplicated(['MyColumnName'], keep=False)]

# alternative 
mask = df.MyColumnName.duplicated(keep=False)
df_duplicates=df[mask]
df_notduplicates=df[~mask]

# get unique values
df_unique=df.drop_duplicates(subset="MyColumnName", keep='first', inplace=False)
