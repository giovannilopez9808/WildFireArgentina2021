from modules.DavisData import DavisData
from pandas import read_csv
from os.path import join

data = DavisData()
data = data._read()
dates= sorted(set(
    data.index.date
))
for date in dates:
    print("="*30)
    print(date)
    print(
        data[
            data.index.date == date
        ]
    )
