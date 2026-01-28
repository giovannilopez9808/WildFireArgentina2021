from functools import reduce
from operator import and_
from os.path import join
from typing import (
    List,
    Set,
)
from pandas import (
    Timestamp,
    to_datetime,
    DataFrame,
    concat,
    read_csv,
)


class _DavisBaseData:
    def __init__(
        self,
        columns: List[str],
    ) -> None:
        self.folder = join(
            "..",
            "data",
            "davis",
        )
        self.files = dict(
            ISANTAFE117=dict(
                date_i=to_datetime("2021-01-01"),
                date_f=to_datetime("2022-01-01"),
            ),
            IROSAR70=dict(
                date_i=to_datetime("2021-01-01"),
                date_f=to_datetime("2022-01-01"),
            ),
            IROSAR56=dict(
                date_i=to_datetime("2021-01-01"),
                date_f=to_datetime("2022-01-01"),
            ),
        )
        self.wind_dictionary = dict(
            NNE=dict(
                limits=[12, 34],
                direction=67.5,
            ),
            NE=dict(
                limits=[34, 56],
                direction=45,
            ),
            ENE=dict(
                limits=[56, 78],
                direction=22.5,
            ),
            E=dict(
                limits=[78, 100],
                direction=0,
            ),
            ESE=dict(
                limits=[100, 122],
                direction=337.5,
            ),
            SE=dict(
                limits=[122, 144],
                direction=315,
            ),
            SSE=dict(
                limits=[144, 166],
                direction=292.5,
            ),
            S=dict(
                limits=[166, 188],
                direction=270,
            ),
            SSW=dict(
                limits=[188, 210],
                direction=247.5,
            ),
            SW=dict(
                limits=[210, 232],
                direction=225,
            ),
            WSW=dict(
                limits=[232, 254],
                direction=202.5,
            ),
            W=dict(
                limits=[254, 276],
                direction=180,
            ),
            WNW=dict(
                limits=[276, 298],
                direction=157.5,
            ),
            NW=dict(
                limits=[298, 320],
                direction=135
            ),
            NNW=dict(
                limits=[320, 342],
                direction=112.5,
            ),
            N=dict(
                limits=[342, 34],
                direction=90,
            ),
        )
        self.columns = columns
        # self.columns += [
        # "obsTimeLocal"
        # ]

    @staticmethod
    def _get_wind_direction_numeric(
        value: float,
        wind_dictionary: dict,
    ) -> str:
        wind_dictionary = list(
            wind_dictionary.items()
        )
        for name, params in wind_dictionary[:-1]:
            direction = params["direction"]
            limits = params["limits"]
            is_in_limit = value >= limits[0] and value <= limits[-1]
            if is_in_limit:
                return direction
        return 90

    @staticmethod
    def _get_wind_direction(
        value: float,
        wind_dictionary: dict,
    ) -> str:
        wind_dictionary = list(
            wind_dictionary.items()
        )
        for name, params in wind_dictionary[:-1]:
            limits = params["limits"]
            is_in_limit = value >= limits[0] and value <= limits[-1]
            if is_in_limit:
                return name
        return "N"

    def _fill_wind_direction(
        self,
        data: DataFrame,
    ) -> DataFrame:
        data["winddirStr"] = data["winddirAvg"].apply(
            lambda value:
            self._get_wind_direction(
                value,
                self.wind_dictionary,
            )
        )
        data["winddirNum"] = data["winddirAvg"].apply(
            lambda value:
            self._get_wind_direction_numeric(
                value,
                self.wind_dictionary,
            )
        )
        return data

    @staticmethod
    def _get_dates(
        data: DataFrame,
    ) -> Set[Timestamp]:
        dates = set(
            data.index.date
        )
        return dates

    @staticmethod
    def _get_condition(
        data: DataFrame,
        dates: Set[Timestamp],
    ) -> DataFrame:
        conditions = list(
            data.index.date != date
            for date in dates
        )
        if len(conditions) > 0:
            condition = reduce(
                and_,
                conditions,
            )
            data = data[
                condition
            ]
        return data

    def read(
        self,
    ) -> DataFrame:
        data = list()
        dates = set()
        for file, _ in self.files.items():
            file = f"{file}.csv"
            file = join(
                self.folder,
                file,
            )
            _data = read_csv(
                file,
                index_col="obsTimeLocal",
                parse_dates=True,
            )
            _data = _data[
                self.columns
            ]
            _data = _data.dropna()
            _dates = self._get_dates(
                _data,
            )
            _data = self._get_condition(
                _data,
                dates,
            )
            dates = dates.union(
                _dates,
            )
            data.append(
                _data,
            )
        data = concat(
            data,
        )
        if "winddirAvg" in self.columns:
            data = self._fill_wind_direction(
                data,
            )
        return data


class _DavisWindData(
    _DavisBaseData
):
    def __init__(
        self,
    ) -> None:
        super().__init__(
            columns=[
                "winddirAvg",
                "windspeedAvg",
            ],
        )


class _DavisMeteorologicalData(
    _DavisBaseData
):
    def __init__(
        self,
    ) -> None:
        super().__init__(
            columns=[
                'humidityAvg',
                'tempAvg',
                'pressureMax',
                'pressureMin',
                'precipTotal',
            ],
        )


class DavisData:
    def __init__(
        self,
    ) -> None:
        self.wind_dictionary: dict = None

    def _get_meteorological_data(
        self,
    ) -> DataFrame:
        dataset = _DavisMeteorologicalData()
        data = dataset.read()
        self.wind_dictionary = dataset.wind_dictionary
        return data

    @staticmethod
    def _get_wind_data(
    ) -> DataFrame:
        dataset = _DavisWindData()
        data = dataset.read()
        return data

    def read(
        self,
    ) -> DataFrame:
        meteorological_data = self._get_meteorological_data()
        wind_data = self._get_wind_data()
        data = concat(
            [
                meteorological_data,
                wind_data,
            ],
            axis=1,
        )
        return data
