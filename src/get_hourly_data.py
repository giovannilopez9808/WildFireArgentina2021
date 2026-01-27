from modules.DavisData import DavisData
from os.path import join
from pandas import (
    DataFrame,
    read_csv,
    concat,
    merge,
    set_option,
    to_datetime,
)
set_option('display.max_colwidth', None)


def get_values_in_str(
    data: DataFrame,
    params: dict,
) -> DataFrame:
    for column, _params in params["final_columns"].items():
        if _params["has_std"]:
            mean_column = f"{column}_mean"
            std_column = f"{column}_std"
            data[column] = data[[
                mean_column,
                std_column,
            ]].apply(
                lambda values:
                f"{values[mean_column]}±{values[std_column]}",
                axis=1,
            )
            data = data.drop(
                columns=[
                    mean_column,
                    std_column,
                ],
            )
        data = data.rename(
            columns={
                column: _params["name"],
            },
        )
    return data


params = dict(
    columns=[
        "humidityAvg",
        "tempAvg",
        "windspeedAvg",
        "pressureMin",
        "pressureMax",
    ],
    final_columns=dict(
        NI=dict(
            name="Fire",
            has_std=False,
        ),
        winddirStr=dict(
            name="Wind direction",
            has_std=False,
        ),
        windspeedAvg=dict(
            name="Wind speed (km/hr)",
            has_std=True,
        ),
        tempAvg=dict(
            name="Temperature",
            has_std=True,
        ),
        humidityAvg=dict(
            name="Humidity",
            has_std=True,
        ),
        pressureAvg=dict(
            name="Pressure (hPa)",
            has_std=True,
        ),
    ),
)

dataset = DavisData()
data = dataset.read()
_data = data[
    params["columns"]
]
_data.loc[:, "pressureAvg"] = _data[[
    "pressureMax",
    "pressureMin"
]].mean(
    axis=1,
)
_data = _data.drop(
    columns=[
        "pressureMin",
        "pressureMax",
    ],
)
_data["tempAvg"] = _data["tempAvg"].apply(
    lambda value:
    (value-32)/1.8,
)
daily_mean = _data.resample(
    "D"
).mean()
daily_std = _data.resample(
    "D"
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
daily_data = daily_data.round(1)
_data = data[[
    "winddirStr"
]]
_data["date"] = list(
    date.strftime(
        "%Y-%m-%d"
    )
    for date in _data.index
)
print(
    _data[
        _data["date"] == "2021-02-26"
    ]
)
_data = _data.groupby(
    [
        "date",
        "winddirStr",
    ],
).size()
_data = _data.reset_index()
_data = _data.sort_values(
    by=[
        "date",
        0,
    ],
    ascending=False,
)
exit(1)
# print(_data)
_data = _data.loc[
    _data.groupby(
        "date"
    )[0].idxmax()
]
_data.index = _data["date"]
_data = _data[[
    "winddirStr",
]]
_data = _data.sort_index()
daily_data = concat(
    [

        daily_data,
        _data,
    ],
    axis=1,
)
filename = join(
    "..",
    "data",
    "fire",
    "data.csv",
)
data = read_csv(
    filename,
    parse_dates=True,
    index_col=0,
)
data.index = list(
    date.strftime(
        "%Y-%m-%d"
    )
    for date in data.index
)
daily_data = concat(
    [
        daily_data,
        data,
    ],
    axis=1,
    join="inner",
)
daily_data = get_values_in_str(
    daily_data,
    params,
)
daily_data = daily_data.sort_index()
filename = join(
    "..",
    "result",
    "daily_data.csv",
)
print(daily_data)
daily_data.index.name = "Date"
daily_data.to_csv(
    filename,
)
