from sklearn.linear_model import LinearRegression
from matplotlib import pyplot
from pandas import read_csv
from os.path import join
from numpy import array

filename = join(
    "..",
    "data",
    "propietary",
    "data.csv"
)
data = read_csv(
    filename,
    parse_dates=True,
    index_col=0,
    date_format="%d/%m/%Y",
)
model = LinearRegression(
    fit_intercept=False,
)
input_data = data["Optical Method mean"].to_numpy()
input_data = input_data.reshape(
    -1,
    1,
)
output_data = data["Gravimetric Method"].to_numpy()
output_data = output_data.reshape(
    -1,
    1,
)
model = model.fit(
    input_data,
    output_data,
)
input_data = array([
    0,
    160,
])
input_data = input_data.reshape(
    -1,
    1,
)
output_data = model.predict(
    input_data,
)
pyplot.scatter(
    data["Optical Method mean"],
    data["Gravimetric Method"],
)
pyplot.plot(
    input_data,
    output_data,
)
pyplot.xlabel(
    "Optical method"
)
pyplot.ylabel(
    "Gravimetric method"
)
pyplot.savefig(
    "test.png"
)
