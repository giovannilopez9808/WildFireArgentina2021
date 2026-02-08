import matplotlib.patheffects as PathEffects
from modules.DavisData import DavisData
from matplotlib import pyplot
from numpy import linspace
from os.path import join
from pandas import (
    date_range,
    DataFrame,
    read_csv,
    to_datetime,
)
from numpy import (
    linspace,
    round,
    pi,
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
dataset = DavisData()
data = dataset.read()
dates = date_range(
    "2021-01-01",
    "2021-12-31",
    freq="D",
)
degrees_str = list(
    dataset.wind_dictionary.keys()
)
degrees = list(
    dictionary["direction"]
    for dictionary in dataset.wind_dictionary.values()
)
ticks = list(
    zip(
        degrees,
        degrees_str,
    )
)
ticks = sorted(
    ticks,
    key=lambda value: value[0]
)
degrees = list(
    values[0]*pi/180
    for values in ticks
)
degrees_str = list(
    values[-1]
    for values in ticks
)
for date in dates:
    # date = to_datetime(
    # "2021-10-29"
    # )
    daily_data = data[
        data.index.date == date.date()
    ]
    fig, ax = pyplot.subplots(
        figsize=(
            11,
            11,
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
    max_number = results["Count"].max()
    max_number = (max_number//10)*10
    yticks = linspace(
        10,
        max_number,
        4,
    )
    yticks = round(
        yticks,
    )
    bars = ax.bar(
        (bins+180)*pi/180,
        results["Count"],
        color="#FFB700",
        width=0.3,
    )
    for spine in ax.spines.values():
        spine.set_edgecolor('white')
        spine.set_linewidth(3)
    ax.set_xticks(
        degrees,
    )
    ticks = ax.set_xticklabels(
        degrees_str,
        weight="bold",
        color="white",
    )
    list(
        tick.set_path_effects(
            [
                PathEffects.withStroke(
                    foreground='black',
                    linewidth=5,
                )
            ]
        )
        for tick in ticks
    )
    ax.set_yticks(
        yticks,
    )
    ax.set_yticklabels(
        list(
            int(ytick)
            for ytick in yticks
        ),
        weight="bold",
    )
    ax.set_ylim(
        0,
        max_number*1.25,
    )
    ax.tick_params(
        labelsize=27,
        axis="x",
        pad=32,
    )
    ax.tick_params(
        labelsize=25,
        axis="y",
    )
    # ax.set_xlabel(
    # date.strftime(
    # "%Y-%m-%d"
    # ),
    # weight="bold",
    # fontsize=26,
    # )
    ax.grid(
        color="#ffffff",
        lw=3,
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
        transparent=True,
    )
    pyplot.close()
