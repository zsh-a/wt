import pandas as pd

df = pd.read_csv('000001.csv')

print(df)

df = df.rename(columns={'open':'<Open>','high':'<High>','low':'<Low>','close':'<Close>','volume':'<Volume>'})

df['datetime'] = pd.to_datetime(df['datetime'])
# 提取日期和时间
df['<Date>'] = df['datetime'].dt.date
df['<Time>'] = df['datetime'].dt.time
# df.index = pd.to_datetime(df.index, format='%Y/%m/%d %H:%M:%S')
del df['datetime']
print(df)
df.to_csv('ETF.000001.csv',index=False)