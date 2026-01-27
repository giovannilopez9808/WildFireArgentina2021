from modules.DavisData import DavisData
from matplotlib import pyplot
from numpy import linspace
from os.path import join
from numpy import pi
from pandas import (
    date_range,
    to_datetime,
    DataFrame,
    read_csv,
)


filename = join(
    "..",
    "data",
    "propietary",
    "data.csv",
)
propietary = read_csv(
    filename,
    date_format="%d/%m/%Y",
    parse_dates=True,
    index_col=0,
)
# propietary = propietary[
# propietary["Gravimetric Method"] >= 45
# ]
dataset = DavisData()
data = dataset.read()
dates = date_range(
    "2021-01-01",
    "2021-12-31",
    freq="D",
)
for date in dates:
    daily_data = data[
        data.index.date == date.date()
    ]
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
        _data = daily_data[
            (daily_data["winddirNum"] >= inf+180) &
            (daily_data["winddirNum"] < sup+180)
        ]
        count = _data["winddirNum"].count()
        results.loc[inf+180] = count
    bins = bins[:-1]
    ax.bar(
        (bins+180)*pi/180,
        results["Count"],
        # align="edge",
        color="#FFB700",
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
        dataset.wind_dictionary.keys()
    )
    ax.tick_params(
        labelsize=25,
        pad=30,
    )
    fig.tight_layout(
        pad=4,
    )
    filename = date.strftime(
        "%Y-%m-%d.png"
    )
    filename = join(
        "..",
        "graphics",
        "wind_direction",
        filename,
    )
    pyplot.savefig(
        filename,
    )
    pyplot.close()
    exit(1)
