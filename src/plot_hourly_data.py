from modules.DavisData import DavisData
from os.path import join
from pandas import (
    Series,
    merge,
    concat,
)

dataset = DavisData()
data = dataset.read()
_data = data[[
    "humidityAvg",
    "tempAvg",
    "windspeedAvg",
    "pressureMin",
    "pressureMax",
]]
_data.loc[:,"pressureAvg"] = _data[[
    "pressureMax",
    "pressureMin"
]].mean(
    axis=1,
)
daily_mean = _data.resample(
    "d"
).mean()
daily_std = _data.resample(
    "d"
).std()
daily_data = merge(
    daily_mean,
    daily_std,
    left_on=daily_mean.index,
    right_on=daily_std.index,
    suffixes=(
        '_mean',
        '_std',
    ),
)
daily_data = daily_data.dropna()
daily_data = daily_data.set_index(
    "key_0",
)
daily_data.index = list(
    date.strftime(
        "%Y-%m-%d"
    )
    for date in daily_data.index
)
daily_data = daily_data.round()
_data = data[[
    "winddirStr"
]]
_data["date"] = list(
    date.strftime(
        "%Y-%m-%d"
    )
    for date in _data.index
)
_data = _data.groupby(
    [
        "date",
        "winddirStr",
    ],
).size()
_data = _data.reset_index()
_data = _data.groupby(
    "date"
).max()
_data = _data[[
    "winddirStr",
]]
_data = _data.dropna()
daily_data = concat(
    [

        daily_data,
        _data,
    ],
    axis=1,
)
filename = join(
    "..",
    "result",
    "daily_data.csv",
)
daily_data.index.name = "Date"
daily_data.to_csv(
    filename,
)
