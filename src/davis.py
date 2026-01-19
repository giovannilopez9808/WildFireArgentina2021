from pandas import read_csv
from os.path import join

filename = join(
    "..",
    "data",
    "davis",
    "202101.csv"
)
data = read_csv(
    filename,
)
print(data)
