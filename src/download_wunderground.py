from dotenv import load_dotenv
from os.path import join
from tqdm import tqdm
from os import getenv
from pandas import (
    DataFrame,
    read_csv,
    concat,
)
import requests


load_dotenv()
# stationid="ISANTAFE117"
# stationid="IROSAR70"
stationid="IROSAR56"
general_endpoint = getenv(
    "endpoint_wunderground"
)
filename = join(
    "..",
    "data",
    "propietary",
    "data.csv",
)
measurements = read_csv(
    filename,
    index_col=0,
    parse_dates=True,
    date_format="%d/%m/%Y",
)
data = list()
for index in tqdm(
    measurements.index
):
    date = index.strftime(
        "%Y%m%d"
    )
    endpoint = general_endpoint.replace(
        "__date__",
        date,
    )
    endpoint = endpoint.replace(
        "__stationid__",
        stationid,
    )
    response = requests.get(
        endpoint
    )
    response = response.json()
    response = response["observations"]
    list(
        _response.update(
            _response["imperial"]
        )
        for _response in response
    )
    _data = DataFrame(
        response,
    )
    if _data.size>0:
        data.append(
            _data,
        )
data = concat(
    data,
)
# columns = list(
# data.columns[-23:]
# )
# columns += [
# "obsTimeLocal"
# ]
# data = data[
# columns
# ]
data = data.drop(
    columns="imperial",
)
filename = f"{stationid}.csv"
filename = join(
    "..",
    "data",
    "davis",
    filename,
)
data.to_csv(
    filename,
    index=False,
)
