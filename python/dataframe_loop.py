
### 
# This one is ineficient and "dirty", but sometimes it's quicker to just get it done. I mod this if needed if performance is not an issue.
# fill NaN if needed
df['colname']= df['colname'].fillna(value="")
for index in df.index:
    myStr = df.loc[index, 'colname']
    if 'mysubstring' in myStr:
        df.loc[index, 'colname'] = "some value I want to assign"
        
### NESTED FOR LOOP - OPTION 2
iris = pd.read_csv('https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv')

columns = ['sepal_length','sepal_width','petal_length','petal_width']
# columns = list(iris.columns)[0:4] #first 4 column labels

for indices, row in iris.iterrows():
    for column in columns:
        iris.at[indices,column] = row[column] + 2
        
iris.head()
