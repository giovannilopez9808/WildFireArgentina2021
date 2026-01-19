from modules.DavisData import DavisData
from matplotlib import pyplot
from numpy import linspace
from pandas import (
    to_datetime,
    DataFrame,
)
from numpy import (
    pi
)


dataset = DavisData()
data = dataset.read()
data = data[
    data.index.date == to_datetime("2021-06-21").date()
]
print(data)
fig, ax = pyplot.subplots(
    figsize=(
        10, 10
    ),
    subplot_kw=dict(
        projection='polar'
    ),
)
bins = linspace(
    -180,
    180,
    17,
)
results = DataFrame(
    index=bins[:-1]+180,
    columns=["Count"]
)
for inf, sup in zip(
    bins[:-1],
    bins[1:],
):
    _data = data[
        (data["winddirAvg"] >= inf+180) &
        (data["winddirAvg"] < sup+180)
    ]
    count = _data["winddirAvg"].count()
    results.loc[inf+180] = count
bins = bins[:-1]
ax.bar(
    (bins+180)*pi/180,
    results["Count"],
    # align="edge",
    color="#ff8fab",
    width=0.3,
)
# ax.set_ylim(
# 0,
# 30,
# )
# ax.set_yticks(
# range(
# 0,
# 30,
# 5,
# )
# )
ax.set_xticks(
    (bins+180)*pi/180,
)
ax.set_xticklabels(
    dataset.direction_to_degree.keys()
)
ax.tick_params(
    labelsize=25,
    pad=30,
)
fig.tight_layout(
    pad=4,
)
pyplot.savefig(
    "test.png"
)
