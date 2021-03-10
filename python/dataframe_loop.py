
# This one is ineficient and "dirty", but sometimes it's quicker to just get it done. I mod this if needed if performance is not an issue.
# fill NaN if needed
df['colname']= df['colname'].fillna(value="")

for index in df.index:
    myStr = df.loc[index, 'colname']
    if 'mysubstring' in myStr:
        df.loc[index, 'colname'] = "some value I want to assign"
