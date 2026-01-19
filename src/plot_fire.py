from matplotlib import pyplot
from pandas import read_csv
from os.path import join

filename = join(
    "..",
    "data",
    "fire",
    "data.csv",
)
fire = read_csv(
    filename,
    index_col=0,
    parse_dates=True,
)
filename = join(
    "..",
    "data",
    "propietary",
    "data.csv",
)
data = read_csv(
    filename,
    index_col=0,
    parse_dates=True,
    date_format="%d/%m/%Y",
)
fire = fire[
    fire.index.year == 2021
]
fig,ax1 = pyplot.subplots()
ax2 = ax1.twinx()
ax1.plot(
    fire.index,
    fire["NI"],
)
ax2.scatter(
    data.index,
    data["Optical Method mean"],
    color="red",
)
pyplot.savefig(
    "test.png"
)
