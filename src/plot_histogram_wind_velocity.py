from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from pandas.tseries.offsets import Hour
from modules.DavisData import DavisData
from matplotlib import pyplot
from pandas import (
    to_timedelta,
    to_datetime,
)


dataset = DavisData()
data = dataset.read()
print(data.columns)
data = data[[
    "windspeedAvg"
]]
# hourly_data = data.resample("h").mean()
hourly_data = data
mean = data.mean()
print(mean)
daily_data = data.resample("D").mean()
fig, ax = pyplot.subplots(
    figsize=(
        10, 4
    )
)
count, bins, patch = ax.hist(
    hourly_data["windspeedAvg"],
    color="#9d4edd",
    align="mid",
    rwidth=0.95,
    bins=9,
)
ax.axvline(
    mean["windspeedAvg"],
    color="#fb8500",
    alpha=0.75,
    ls="--",
)
ax.set_xlabel(
    "Velocidad del viento (m/s)",
    fontsize=17,
)
ax.set_ylabel(
    "Frecuencia (horas)",
    fontsize=17,
)
ax.set_xticks(
    bins,
)
ax.set_xlim(
    0,
    16.5,
)
ax.set_ylim(
    0,
    5000,
)
# ax.text(
# 0.25,
# 1000,
# "a)",
# fontsize=16,
# )
ax.tick_params(
    labelsize=14,
)
# sub_ax = inset_axes(
# parent_axes=ax,
# height="50%",
# width="70%",
# borderpad=2,
# )
# sub_ax.plot(
# daily_data["windspeedAvg"],
# color="#38a3a5"
# )
# for month in range(6, 9):
# sub_ax.axvline(
# to_datetime(
# f"2020-0{month}-01"
# ),
# color="#000000",
# alpha=0.7,
# ls="--",
# )
# sub_ax.set_ylabel(
# "Promedio diario de la\nvelocidad del viento (m/s)"
# )
# sub_ax.set_xlim(
# to_datetime(
# "2020-06-01"
# ),
# to_datetime(
# "2020-08-31"
# ),
# )
# sub_ax.set_ylim(
# 0,
# 9,
# )
# ticks = list(
# to_datetime(
# "2020-06-01"
# )+to_timedelta(
# tick*7,
# unit="d"
# )
# for tick in range(14)
# )
# ticks_label = list(
# tick.strftime("%d/%m")
# for tick in ticks
# )
# sub_ax.set_xticks(
# ticks,
# )
# sub_ax.set_xticklabels(
# ticks_label,
# fontsize=9,
# )
# sub_ax.set_yticks(
# range(
# 0,
# 12,
# 3
# )
# )
# sub_ax.tick_params(
# labelsize=9,
# )
# sub_ax.text(
# to_datetime(
# "2020-06-03",
# ),
# 7,
# "b)",
# fontsize=14,
# )
fig.tight_layout()
pyplot.savefig(
    "test.png"
)
